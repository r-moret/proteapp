from fastapi import APIRouter, Depends, HTTPException
from proteapp.models.people import Person
from proteapp.api.users.schemas import PublicUser, CreateUser

from proteapp.models.users import User
from proteapp.api.deps import get_sql_session
from sqlmodel import Session, select

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/search", response_model=list[PublicUser])
def get_users(session: Session = Depends(get_sql_session)):
    return session.exec(select(User)).all()


@router.post("/", response_model=PublicUser, status_code=201)
def post_user(user: CreateUser, session: Session = Depends(get_sql_session)):
    user_db = User.model_validate(user)

    person_db = session.get(Person, user.person_id)

    if not person_db:
        raise HTTPException(404, "No person found")

    person_db.users.append(user_db)

    session.add(person_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@router.delete("/{id}")
def delete_user(id: int, session: Session = Depends(get_sql_session)):
    user_db = session.get(User, id)

    if user_db is None:
        raise HTTPException(404, "No user found")

    session.delete(user_db)
    session.commit()
