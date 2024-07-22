from proteapp.models.base import ULIDSchema
from proteapp.models.sql.adoptions import AdoptionKind
from datetime import date


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
