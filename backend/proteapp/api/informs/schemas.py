from datetime import date, datetime
from typing import Optional
from pydantic import Field
from proteapp.models.base import ULIDSchema, BaseSchema
from ulid import ULID


class ListedInform(ULIDSchema):
    class User(ULIDSchema):
        class Person(BaseSchema):
            name: str
            first_surname: str
            second_surname: str | None

        person: Person

    class TimeRange(BaseSchema):
        class Time(BaseSchema):
            hours: int
            minutes: int

        start: Time
        end: Time

    creator: User
    volunteers: list[User]
    date: date
    time_range: TimeRange


class CompleteInform(ListedInform):
    class Animal(ULIDSchema):
        name: str

    class Note(BaseSchema):
        class Yard(ULIDSchema):
            name: str

        yard: Optional[Yard] = None
        animal: "CompleteInform.Animal"
        text: str = Field(min_length=1)

    class Visit(BaseSchema):
        visitor: str = Field(min_length=1)
        description: str = Field(min_length=1)

    class Arrival(BaseSchema):
        name: str = Field(min_length=1)
        description: Optional[str] = Field(default=None, min_length=1)

    class Loss(BaseSchema):
        animal: "CompleteInform.Animal"

    class Adoption(BaseSchema):
        animal: "CompleteInform.Animal"
        foster: bool

    class TestedAnimal(BaseSchema):
        animal: "CompleteInform.Animal"
        compatible: bool

    notes: list[Note]
    highlights: Optional[list[str]] = None
    visits: Optional[list[Visit]] = None
    arrivals: Optional[list[Arrival]] = None
    losses: Optional[list[Loss]] = None
    adoptions: Optional[list[Adoption]] = None
    tested_animals: Optional[list[TestedAnimal]] = None


class EditableInform(BaseSchema):
    class Note(BaseSchema):
        animal: ULID
        text: str = Field(min_length=1)

    class Visit(BaseSchema):
        visitor: str = Field(min_length=1)
        description: str = Field(min_length=1)

    class Arrival(BaseSchema):
        name: str = Field(min_length=1)
        description: Optional[str] = Field(default=None, min_length=1)

    class Loss(BaseSchema):
        animal: ULID

    class Adoption(BaseSchema):
        animal: ULID
        foster: bool

    class TestedAnimal(BaseSchema):
        animal: ULID
        compatible: bool

    class TimeRange(BaseSchema):
        class Time(BaseSchema):
            hours: int
            minutes: int

        start: Time
        end: Time

    creator: ULID
    volunteers: list[ULID]
    date: date | datetime
    time_range: TimeRange
    notes: list[Note]
    highlights: Optional[list[str]] = None
    visits: Optional[list[Visit]] = None
    arrivals: Optional[list[Arrival]] = None
    losses: Optional[list[Loss]] = None
    adoptions: Optional[list[Adoption]] = None
    tested_animals: Optional[list[TestedAnimal]] = None
