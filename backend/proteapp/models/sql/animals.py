from sqlmodel import Field, Relationship
from datetime import date
from enum import StrEnum
from proteapp.models.base import SQLULIDSchema, SQLAlchemyULIDType
from typing import TYPE_CHECKING, Optional
from ulid import ULID

if TYPE_CHECKING:
    from proteapp.models.sql.treatments import Treatment
    from proteapp.models.sql.appointments import Appointment
    from proteapp.models.sql.yards import Yard


class Sex(StrEnum):
    male = "male"
    female = "female"


class Animal(SQLULIDSchema, table=True):
    name: str
    sex: Sex
    personality: str | None = Field(default=None)
    description: str | None = Field(default=None)
    birth_date: date | None = Field(default=None)
    entry_date: date | None = Field(default=None)
    is_animal_compatible: bool | None = Field(default=None)
    is_castrated: bool | None = Field(default=None)
    image: str | None = Field(default=None)

    yard_id: ULID | None = Field(default=None, foreign_key="yard.id", sa_type=SQLAlchemyULIDType)

    treatments: list["Treatment"] = Relationship(back_populates="animal")
    appointments: list["Appointment"] = Relationship(back_populates="animal")
    yard: Optional["Yard"] = Relationship(back_populates="animals")
