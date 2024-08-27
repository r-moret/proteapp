from fastapi import APIRouter, HTTPException, Depends, UploadFile
from sqlmodel import Session, select
from proteapp.api.animals.schemas import ListedAnimal, CompleteAnimal, EditableAnimal
from proteapp.models.sql.animals import Animal
from proteapp.api.deps import get_sql_session, save_image
from ulid import ULID
from proteapp.api.animals.adapters import to_animal
from pydantic import ValidationError
from pathlib import Path

router = APIRouter(prefix="/animal", tags=["animal"])


@router.get("/search", response_model=list[ListedAnimal])
def get_animals(session: Session = Depends(get_sql_session)):
    animals = session.exec(select(Animal)).all()
    return animals


@router.post("/", response_model=CompleteAnimal, status_code=201)
def post_animal(animal: EditableAnimal, session: Session = Depends(get_sql_session)):
    try:
        animal_db = to_animal(animal)
    except ValidationError:
        raise HTTPException(422, "Unable to create a new animal with the data passed")

    session.add(animal_db)
    session.commit()
    session.refresh(animal_db)

    return animal_db


@router.post("/{id}/image", response_model=CompleteAnimal)
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


@router.delete("/{id}/image", response_model=CompleteAnimal)
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


@router.put("/{id}", response_model=CompleteAnimal)
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


@router.delete("/{id}", status_code=204)
def delete_animal(id: ULID, session: Session = Depends(get_sql_session)):
    animal_db = session.get(Animal, id)

    if animal_db is None:
        raise HTTPException(404, "No animal found")

    session.delete(animal_db)
    session.commit()
