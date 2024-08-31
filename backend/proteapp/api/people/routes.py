from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.people.schemas import EditablePerson, CompletePerson

from proteapp.models.sql.people import Person
from proteapp.api.deps import get_sql_session, admin_required
from sqlmodel import Session, select
from ulid import ULID

router = APIRouter(prefix="/person", tags=["person"])


@router.get("/search", response_model=list[CompletePerson])
def get_people(session: Session = Depends(get_sql_session)):
    return session.exec(select(Person)).all()


@router.post("/", response_model=CompletePerson, status_code=201)
def post_person(person: EditablePerson, session: Session = Depends(get_sql_session)):
    person_db = Person.model_validate(person)

    session.add(person_db)
    session.commit()
    session.refresh(person_db)

    return person_db


@router.get("/{id}", response_model=CompletePerson)
def get_person(id: ULID, session: Session = Depends(get_sql_session)):
    person_db = session.get(Person, id)

    if person_db is None:
        raise HTTPException(404, "Person not found")

    return person_db


@router.put("/{id}", response_model=CompletePerson, dependencies=[Depends(admin_required)])
def put_person(id: ULID, person: EditablePerson, session: Session = Depends(get_sql_session)):
    person_db = session.get(Person, id)

    if person_db is None:
        raise HTTPException(404, "Person not found")

    # No need to parse person (EditablePerson) into Person
    # because they share all their attributes
    person_db.sqlmodel_update(person)

    session.add(person_db)
    session.commit()
    session.refresh(person_db)

    return person_db


@router.delete("/{id}", dependencies=[Depends(admin_required)])
def delete_person(id: ULID, session: Session = Depends(get_sql_session)):
    person_db = session.get(Person, id)

    if person_db is None:
        raise HTTPException(404, "Person not found")

    session.delete(person_db)
    session.commit()
