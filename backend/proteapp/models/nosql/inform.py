from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from beanie import Document


class Note(BaseModel):
    yard: Optional[int] = None
    animal: int
    text: str = Field(min_length=1)


class Visit(BaseModel):
    visitor: str = Field(min_length=1)
    description: str = Field(min_length=1)


class Arrival(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)


class Loss(BaseModel):
    animal: int


class Adoption(BaseModel):
    animal: int
    foster: bool


class TestedAnimal(BaseModel):
    animal: int
    compatible: bool


class BaseInform(BaseModel):
    creator: int
    volunteers: list[int]
    start_time: datetime
    end_time: datetime
    highlights: Optional[list[str]] = None
    notes: list[Note]
    visits: Optional[list[Visit]] = None
    arrivals: Optional[list[Arrival]] = None
    losses: Optional[list[Loss]] = None
    adoptions: Optional[list[Adoption]] = None
    tested_animals: Optional[list[TestedAnimal]] = None


class Inform(Document, BaseInform):
    class Settings:
        validate_on_save = True
