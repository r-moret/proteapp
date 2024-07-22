from ulid import ULID
from proteapp.models.base import ULIDSchema, BaseSchema
from pydantic_extra_types.phone_numbers import PhoneNumber


class EditableUser(BaseSchema):
    password: str  # TODO: Handle password encryptation and storage
    active: bool
    veteran: bool
    image: str | None = None
    person: ULID


class ListedUser(ULIDSchema):
    class Person(ULIDSchema):
        name: str
        first_surname: str
        second_surname: str | None

    active: bool
    veteran: bool
    image: str | None
    person: Person


class CompleteUser(ListedUser):
    class Person(ULIDSchema):
        name: str
        first_surname: str
        phone: PhoneNumber
        second_surname: str | None
        email: str | None

    person: Person
