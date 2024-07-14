from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.people.schemas import (
  PublicPersonWithRelationships,
  PublicPerson,
  CreatePerson,
  UpdatePerson
)

from proteapp.models.people import Person
from proteapp.api.deps import get_session
from sqlmodel import Session, select

router = APIRouter(prefix="/person", tags=["person"])

@router.get("/search", response_model=list[PublicPersonWithRelationships])
def get_people(session: Session = Depends(get_session)):
    return session.exec(select(Person)).all()


@router.post("/", response_model=PublicPerson, status_code=201)
def post_person(person: CreatePerson, session: Session = Depends(get_session)):
    person_db = Person.model_validate(person)

    session.add(person_db)
    session.commit()
    session.refresh(person_db)

    return person_db

@router.get("/{id}", response_model=PublicPersonWithRelationships)
def get_person(id: int, session: Session = Depends(get_session)):
    person_db = session.get(Person, id)

    if person_db is None:
        raise HTTPException(404, "No person found")

    return person_db

@router.put("/{id}", response_model=PublicPerson)
def put_person(id: int, person: UpdatePerson, session: Session = Depends(get_session)):
    person_db = session.get(Person, id)

    if person_db is None:
        raise HTTPException(404, "No person found")

    person_db.sqlmodel_update(person)

    session.add(person_db)
    session.commit()
    session.refresh(person_db)

    return person_db


@router.delete("/{id}")
def delete_person(id: int, session: Session = Depends(get_session)):
    person_db = session.get(Person, id)

    if person_db is None:
        raise HTTPException(404, "No person found")

    session.delete(person_db)
    session.commit()