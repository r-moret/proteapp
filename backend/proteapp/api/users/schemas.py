from ulid import ULID
from proteapp.models.base import ULIDSchema, BaseSchema


class EditableUser(BaseSchema):
    active: bool
    veteran: bool
    person: ULID


class ListedUser(ULIDSchema):
    class Person(ULIDSchema):
        name: str
        first_surname: str
        email: str
        second_surname: str | None

    active: bool
    veteran: bool
    image: str | None
    person: Person


class CompleteUser(ListedUser):
    class Person(ULIDSchema):
        name: str
        first_surname: str
        phone: str
        second_surname: str | None
        email: str

    person: Person
