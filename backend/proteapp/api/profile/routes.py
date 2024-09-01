from fastapi import APIRouter, Depends, UploadFile
from proteapp.api.users.schemas import CompleteUser
from proteapp.api.people.schemas import CompletePerson, EditablePerson
from proteapp.models.sql.users import User
from proteapp.api.deps import get_sql_session, save_image, get_logged_user_http
from sqlmodel import Session
from pathlib import Path


router = APIRouter(prefix="/profile", tags=["profile"])


@router.put("/person", response_model=CompletePerson)
def update_profile_person(
    person: EditablePerson,
    my_user: User = Depends(get_logged_user_http),
    session: Session = Depends(get_sql_session),
):
    session.add(my_user)
    my_user.person.sqlmodel_update(person)

    session.commit()
    session.refresh(my_user)

    print("Person updated")
    return my_user.person


@router.post("/image", response_model=CompleteUser)
def post_profile_image(
    image: UploadFile,
    my_user: User = Depends(get_logged_user_http),
    session: Session = Depends(get_sql_session),
):
    image_path = save_image(image)

    session.add(my_user)
    if my_user.image:
        Path(my_user.image).unlink(missing_ok=True)

    my_user.image = image_path

    session.commit()
    session.refresh(my_user)

    return my_user


@router.delete("/image", response_model=CompleteUser)
def delete_profile_image(
    my_user: User = Depends(get_logged_user_http),
    session: Session = Depends(get_sql_session),
):
    session.add(my_user)
    if not my_user.image:
        return my_user

    Path(my_user.image).unlink(missing_ok=True)

    my_user.image = None

    session.commit()
    session.refresh(my_user)

    return my_user
