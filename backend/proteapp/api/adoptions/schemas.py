from proteapp.models.base import ULIDSchema, BaseSchema
from proteapp.models.sql.adoptions import AdoptionKind
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import date

from ulid import ULID


class ListedAdoption(ULIDSchema):
    class Animal(ULIDSchema):
        name: str
        image: str | None = None

    class Person(ULIDSchema):
        name: str
        first_surname: str

    register_date: date
    kind: AdoptionKind
    revocation_date: date | None = None
    animal: Animal
    person: Person


class CompleteAdoption(ULIDSchema):
    class Animal(ULIDSchema):
        name: str
        image: str | None = None
        description: str | None = None
        personality: str | None = None
        birth_date: date | None = None
        is_animal_compatible: bool | None = None
        is_castrated: bool | None = None

    class Person(ULIDSchema):
        name: str
        first_surname: str
        phone: PhoneNumber
        second_surname: str | None = None
        email: str | None = None

    class Monitoring(ULIDSchema):
        follow_date: date
        note: str

    register_date: date
    kind: AdoptionKind
    revocation_date: date | None = None
    animal: Animal
    person: Person
    monitorings: list[Monitoring]


class EditableAdoption(BaseSchema):
    register_date: date
    kind: AdoptionKind
    animal: ULID
    person: ULID
