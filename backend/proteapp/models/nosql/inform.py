from odmantic import Model, Field, EmbeddedModel

from datetime import datetime
from bson import ObjectId
from typing import Optional


class Note(EmbeddedModel):
    yard: Optional[int] = None
    animal: int
    text: str = Field(min_length=1)


class Visit(EmbeddedModel):
    visitor: str = Field(min_length=1)
    description: str = Field(min_length=1)


class Arrival(EmbeddedModel):
    name: str = Field(min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)


class Loss(EmbeddedModel):
    animal: int


class Adoption(EmbeddedModel):
    animal: int
    foster: bool


class TestedAnimal(EmbeddedModel):
    animal: int
    compatible: bool


class Inform(Model):
    id: ObjectId = Field(default_factory=ObjectId, primary_field=True)
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
