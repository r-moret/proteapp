from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from proteapp.models.nosql.inform import BaseInform
from beanie import PydanticObjectId


class ListedInform(BaseModel):
    id: PydanticObjectId
    creator: BaseInform.Person
    volunteers: list[BaseInform.Person]
    start_time: datetime
    end_time: datetime


class CompleteInform(BaseInform):
    id: PydanticObjectId


class EditableInform(BaseModel):
    class Note(BaseModel):
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

    creator: int
    volunteers: list[int]
    start_time: datetime
    end_time: datetime
    notes: list[Note]
    highlights: Optional[list[str]] = None
    visits: Optional[list[Visit]] = None
    arrivals: Optional[list[Arrival]] = None
    losses: Optional[list[Loss]] = None
    adoptions: Optional[list[Adoption]] = None
    tested_animals: Optional[list[TestedAnimal]] = None
