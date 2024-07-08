from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from proteapp.models.treatments import Treatment


class Sex(StrEnum):
    male = "male"
    female = "female"


class BaseAnimal(SQLModel):
    name: str
    sex: Sex
    yard: str | None = Field(default=None)
    personality: str | None = Field(default=None)
    description: str | None = Field(default=None)
    birth_date: date | None = Field(default=None)
    entry_date: date | None = Field(default=None)
    is_animal_compatible: bool | None = Field(default=None)
    is_castrated: bool | None = Field(default=None)
    image: str | None = Field(default=None)


class Animal(BaseAnimal, table=True):
    id: int | None = Field(default=None, primary_key=True)

    treatments: list["Treatment"] = Relationship(back_populates="animal")
