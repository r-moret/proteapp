import os
import tempfile
from ulid import ULID
from fastapi import APIRouter, HTTPException, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from proteapp.api.animals.schemas import ListedAnimal, CompleteAnimal, EditableAnimal
from proteapp.models.sql.animals import Animal
from proteapp.api.deps import get_sql_session, save_image, admin_required
from proteapp.api.animals.adapters import to_animal
from proteapp.animal_report import create_report
from pydantic import ValidationError
from pathlib import Path
from starlette.background import BackgroundTask


router = APIRouter(prefix="/animal", tags=["animal"])


@router.get("/report")
def download(session: Session = Depends(get_sql_session)):
    absolute_root_directory = os.path.abspath(".")

    animals = [
        CompleteAnimal.model_validate(
            {
                **dict(animal),
                "yard": animal.yard.model_dump() if animal.yard is not None else None,
                "treatments": [treatment.model_dump() for treatment in animal.treatments],
                "appointments": [appointment.model_dump() for appointment in animal.appointments],
                "image": f"{absolute_root_directory}/{animal.image if animal.image is not None else 'images/dog.png'}",
            }
        )
        for animal in session.exec(select(Animal)).all()
    ]

    tempdir = tempfile.TemporaryDirectory(dir=".")
    report_path = f"{tempdir.name}/report.pdf"
    create_report(animals, report_path)

    return FileResponse(
        report_path,
        media_type="application/pdf",
        background=BackgroundTask(tempdir.cleanup),
    )


@router.get("/search", response_model=list[ListedAnimal])
def get_animals(session: Session = Depends(get_sql_session)):
    animals = session.exec(select(Animal)).all()
    return animals


@router.post(
    "/", response_model=CompleteAnimal, status_code=201, dependencies=[Depends(admin_required)]
)
def post_animal(animal: EditableAnimal, session: Session = Depends(get_sql_session)):
    try:
        animal_db = to_animal(animal)
    except ValidationError:
        raise HTTPException(422, "Unable to create a new animal with the data passed")

    session.add(animal_db)
    session.commit()
    session.refresh(animal_db)

    return animal_db


@router.post("/{id}/image", response_model=CompleteAnimal, dependencies=[Depends(admin_required)])
def post_animal_image(id: ULID, image: UploadFile, session: Session = Depends(get_sql_session)):
    animal_db = session.get(Animal, id)

    if animal_db is None:
        raise HTTPException(404, "Animal not found")

    image_path = save_image(image)

    if animal_db.image:
        Path(animal_db.image).unlink(missing_ok=True)

    animal_db.image = image_path

    session.add(animal_db)
    session.commit()
    session.refresh(animal_db)

    return animal_db


@router.delete(
    "/{id}/image", response_model=CompleteAnimal, dependencies=[Depends(admin_required)]
)
def delete_animal_image(id: ULID, session: Session = Depends(get_sql_session)):
    animal_db = session.get(Animal, id)

    if animal_db is None:
        raise HTTPException(404, "Animal not found")

    if not animal_db.image:
        return animal_db

    Path(animal_db.image).unlink(missing_ok=True)

    animal_db.image = None

    session.add(animal_db)
    session.commit()
    session.refresh(animal_db)

    return animal_db


@router.get("/{id}", response_model=CompleteAnimal)
def get_animal(id: ULID, session: Session = Depends(get_sql_session)):
    animal_db = session.get(Animal, id)

    if animal_db is None:
        raise HTTPException(404, "No animal found")

    return animal_db


@router.put("/{id}", response_model=CompleteAnimal, dependencies=[Depends(admin_required)])
def put_animal(id: ULID, animal: EditableAnimal, session: Session = Depends(get_sql_session)):
    animal_db = session.get(Animal, id)

    if animal_db is None:
        raise HTTPException(404, "No animal found")

    try:
        edited_animal = to_animal(animal)
    except ValidationError:
        raise HTTPException(422, "Unable to edit the animal with the data passed")

    for prop, value in dict(edited_animal).items():
        if prop == "id" or prop == "image":
            continue
        setattr(animal_db, prop, value)

    session.add(animal_db)
    session.commit()
    session.refresh(animal_db)

    return animal_db


@router.delete("/{id}", status_code=204, dependencies=[Depends(admin_required)])
def delete_animal(id: ULID, session: Session = Depends(get_sql_session)):
    animal_db = session.get(Animal, id)

    if animal_db is None:
        raise HTTPException(404, "No animal found")

    session.delete(animal_db)
    session.commit()


# @router.get("/report")
# def get_report(session: Session = Depends(get_sql_session)):
#     return None
