from sqlmodel import Field, Relationship
from proteapp.models.globals import GlobalBaseSQLModel
from datetime import date
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from proteapp.models.treatments import Treatment
    from proteapp.models.appointments import Appointment
    from proteapp.models.yards import Yard


class Sex(StrEnum):
    male = "male"
    female = "female"


class BaseAnimal(GlobalBaseSQLModel):
    name: str
    sex: Sex
    personality: str | None = Field(default=None)
    description: str | None = Field(default=None)
    birth_date: date | None = Field(default=None)
    entry_date: date | None = Field(default=None)
    is_animal_compatible: bool | None = Field(default=None)
    is_castrated: bool | None = Field(default=None)
    image: str | None = Field(default=None)

    yard_id: int | None = Field(default=None, foreign_key="yard.id")


class Animal(BaseAnimal, table=True):
    id: int | None = Field(default=None, primary_key=True)

    treatments: list["Treatment"] = Relationship(back_populates="animal")
    appointments: list["Appointment"] = Relationship(back_populates="animal")
    yard: "Yard" = Relationship(back_populates="animals")
