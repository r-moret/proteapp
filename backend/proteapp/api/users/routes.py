from fastapi import APIRouter, Depends, HTTPException
from proteapp.api.users.schemas import ListedUser, CompleteUser, EditableUser
from proteapp.exceptions import UnsavedDataError
from pydantic import ValidationError
from proteapp.models.sql.users import User
from proteapp.api.deps import get_sql_session
from sqlmodel import Session, select
from ulid import ULID
from proteapp.api.users.adapters import to_user
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/search", response_model=list[ListedUser])
def get_users(session: Session = Depends(get_sql_session)):
    return session.exec(select(User)).all()


@router.post("/", response_model=CompleteUser, status_code=201)
def post_user(user: EditableUser, session: Session = Depends(get_sql_session)):
    try:
        user_db = to_user(user)
    except UnsavedDataError as e:
        raise HTTPException(
            422, f"The field {e.field} makes reference to an entity that is not saved yet"
        )
    except ValidationError:
        raise HTTPException(422, "Unable to create an user with the data passed")

    try:
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
    except IntegrityError as e:
        if "UNIQUE" in str(e):
            raise HTTPException(422, "The person specified already has an user")

        raise e

    return user_db


@router.get("/{id}", response_model=CompleteUser)
def get_user(id: ULID, session: Session = Depends(get_sql_session)):
    user_db = session.get(User, id)

    if user_db is None:
        raise HTTPException(404, "User not found")

    return user_db


@router.delete("/{id}")
def delete_user(id: ULID, session: Session = Depends(get_sql_session)):
    user_db = session.get(User, id)

    if user_db is None:
        raise HTTPException(404, "User not found")

    session.delete(user_db)
    session.commit()
