from fastapi import APIRouter, Depends, HTTPException, UploadFile
from proteapp.api.users.schemas import ListedUser, CompleteUser, EditableUser
from proteapp.exceptions import UnsavedDataError
from pydantic import ValidationError
from proteapp.models.sql.users import User
from proteapp.api.deps import (
    get_sql_session,
    save_image,
    admin_required,
    get_register_email_sender,
)
from proteapp.email import EmailSender
from sqlmodel import Session, select
from ulid import ULID
from proteapp.api.users.adapters import to_user
from sqlalchemy.exc import IntegrityError
from passlib.pwd import genword
from pathlib import Path
from typing import cast
from proteapp.api.auth.password import hash_password

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/search", response_model=list[ListedUser])
def get_users(session: Session = Depends(get_sql_session)):
    return session.exec(select(User)).all()


@router.post(
    "/",
    response_model=CompleteUser,
    status_code=201,
    dependencies=[Depends(admin_required)],
)
def post_user(
    user: EditableUser,
    session: Session = Depends(get_sql_session),
    email: EmailSender = Depends(get_register_email_sender),
):
    try:
        user_db = to_user(user)

        user_password = cast(str, genword(length=12))
        user_db.hashed_password = hash_password(user_password)

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

        raise HTTPException(422, "There was an error with the specified data")

    email.send(
        to=user_db.person.email,
        subject="¡Bienvenido a tu nueva cuenta de Proteapp!",
        template_kwargs={
            "name": user_db.person.name,
            "password": user_password,
        },
    )

    return user_db


@router.post("/{id}/image", response_model=CompleteUser, dependencies=[Depends(admin_required)])
def post_user_image(id: ULID, image: UploadFile, session: Session = Depends(get_sql_session)):
    user_db = session.get(User, id)

    if user_db is None:
        raise HTTPException(404, "User not found")

    image_path = save_image(image)

    if user_db.image:
        Path(user_db.image).unlink(missing_ok=True)

    user_db.image = image_path

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@router.delete("/{id}/image", response_model=CompleteUser, dependencies=[Depends(admin_required)])
def delete_user_image(id: ULID, session: Session = Depends(get_sql_session)):
    user_db = session.get(User, id)

    if user_db is None:
        raise HTTPException(404, "User not found")

    if not user_db.image:
        return user_db

    Path(user_db.image).unlink(missing_ok=True)

    user_db.image = None

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@router.get("/{id}", response_model=CompleteUser)
def get_user(id: ULID, session: Session = Depends(get_sql_session)):
    user_db = session.get(User, id)

    if user_db is None:
        raise HTTPException(404, "User not found")

    return user_db


@router.put("/{id}", response_model=CompleteUser, dependencies=[Depends(admin_required)])
def put_user(id: ULID, user: EditableUser, session: Session = Depends(get_sql_session)):
    user_db = session.get(User, id)

    if user_db is None:
        raise HTTPException(404, "User not found")

    try:
        edited_user = to_user(user)
    except ValidationError:
        raise HTTPException(422, "Unable to edit the animal with the data passed")

    for prop, value in dict(edited_user).items():
        if prop == "id" or prop == "image" or prop == "hashed_password":
            continue
        setattr(user_db, prop, value)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@router.delete("/{id}", dependencies=[Depends(admin_required)])
def delete_user(id: ULID, session: Session = Depends(get_sql_session)):
    user_db = session.get(User, id)

    if user_db is None:
        raise HTTPException(404, "User not found")

    session.delete(user_db)
    session.commit()
