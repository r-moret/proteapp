from datetime import date, time
from typing import Optional
from pydantic import Field
from proteapp.models.base import ULIDSchema, BaseSchema, NoSQLULIDSchema
from proteapp.models.time import UTCSchema


class Inform(NoSQLULIDSchema):
    class User(ULIDSchema):
        class Person(BaseSchema):
            name: str
            first_surname: str
            second_surname: Optional[str] = None

        person: Person

    class Animal(ULIDSchema):
        name: str

    class Note(BaseSchema):
        class Yard(ULIDSchema):
            name: str

        yard: Optional[Yard] = None
        animal: "Inform.Animal"
        text: str = Field(min_length=1)

    class Visit(BaseSchema):
        visitor: str = Field(min_length=1)
        description: str = Field(min_length=1)

    class Arrival(BaseSchema):
        name: str = Field(min_length=1)
        description: Optional[str] = Field(default=None, min_length=1)

    class Loss(BaseSchema):
        animal: "Inform.Animal"

    class Adoption(BaseSchema):
        animal: "Inform.Animal"
        foster: bool

    class TestedAnimal(BaseSchema):
        animal: "Inform.Animal"
        compatible: bool

    class TimeRange(UTCSchema, BaseSchema):
        start: time
        end: time

    creator: User
    volunteers: list[User]
    date: date
    time_range: TimeRange
    notes: list[Note]
    highlights: Optional[list[str]] = None
    visits: Optional[list[Visit]] = None
    arrivals: Optional[list[Arrival]] = None
    losses: Optional[list[Loss]] = None
    adoptions: Optional[list[Adoption]] = None
    tested_animals: Optional[list[TestedAnimal]] = None
