from proteapp.api.users.schemas import EditableUser
from proteapp.models.sql.users import User
from sqlmodel import Session
from proteapp.api.deps import sql_engine
from proteapp.models.sql.people import Person
from proteapp.exceptions import UnsavedDataError
from proteapp.api.auth.password import hash_password
from pydantic import ValidationError


def to_user(data: EditableUser) -> User:
    with Session(sql_engine) as session:
        user_person = session.get(Person, data.person)

        if not user_person:
            raise UnsavedDataError(
                "Cannot create an user with a person that doesn't exist", field="person"
            )

        if not data.password:
            raise ValidationError("A password must be passed to create a User")

        return User.model_validate(
            {
                **dict(data),
                "person_id": user_person.id,
                "hashed_password": hash_password(data.password),
            }
        )
