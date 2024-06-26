from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from proteapp.models.animals import (
    PublicAnimal,
    Animal,
    CreateAnimal,
    UpdateAnimal,
    PublicAnimalWithTreatments,
)
from proteapp.api.deps import get_session

router = APIRouter(prefix="/animal", tags=["animal"])


@router.get("/search", response_model=list[PublicAnimal])
def get_animals(session: Session = Depends(get_session)):
    animals = session.exec(select(Animal)).all()
    return animals


@router.post("/", response_model=PublicAnimal, status_code=201)
def post_animal(animal: CreateAnimal, session: Session = Depends(get_session)):
    animal_db = Animal.model_validate(animal)

    session.add(animal_db)
    session.commit()
    session.refresh(animal_db)

    return animal_db


@router.get("/{id}", response_model=PublicAnimalWithTreatments)
def get_animal(id: int, session: Session = Depends(get_session)):
    animal_db = session.get(Animal, id)

    if animal_db is None:
        raise HTTPException(404, "No animal found")

    return animal_db


@router.put("/{id}", response_model=PublicAnimal)
def put_animal(id: int, animal: UpdateAnimal, session: Session = Depends(get_session)):
    animal_db = session.get(Animal, id)

    if animal_db is None:
        raise HTTPException(404, "No animal found")

    animal_db.sqlmodel_update(animal)

    session.add(animal_db)
    session.commit()
    session.refresh(animal_db)

    return animal_db


@router.delete("/{id}")
def delete_animal(id: int, session: Session = Depends(get_session)):
    animal_db = session.get(Animal, id)

    if animal_db is None:
        raise HTTPException(404, "No animal found")

    session.delete(animal_db)
    session.commit()
