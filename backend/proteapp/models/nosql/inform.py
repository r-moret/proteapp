from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from beanie import Document


class BaseInform(BaseModel):
    class Person(BaseModel):
        id: int
        name: str

    class Animal(BaseModel):
        id: int
        name: str

    class Note(BaseModel):
        class Yard(BaseModel):
            id: int
            name: str

        yard: Optional[Yard] = None
        animal: "BaseInform.Animal"
        text: str = Field(min_length=1)

    class Visit(BaseModel):
        visitor: str = Field(min_length=1)
        description: str = Field(min_length=1)

    class Arrival(BaseModel):
        name: str = Field(min_length=1)
        description: Optional[str] = Field(default=None, min_length=1)

    class Loss(BaseModel):
        animal: "BaseInform.Animal"

    class Adoption(BaseModel):
        animal: "BaseInform.Animal"
        foster: bool

    class TestedAnimal(BaseModel):
        animal: "BaseInform.Animal"
        compatible: bool

    creator: Person
    volunteers: list[Person]
    start_time: datetime
    end_time: datetime
    notes: list[Note]
    highlights: Optional[list[str]] = None
    visits: Optional[list[Visit]] = None
    arrivals: Optional[list[Arrival]] = None
    losses: Optional[list[Loss]] = None
    adoptions: Optional[list[Adoption]] = None
    tested_animals: Optional[list[TestedAnimal]] = None


class Inform(BaseInform, Document):
    class Settings:
        validate_on_save = True
