from enum import StrEnum
from proteapp.models.globals import GlobalBaseSQLModel
from datetime import date
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    from proteapp.models.animals import Animal
    from proteapp.models.people import Person

class AdoptionKind(StrEnum):
  permanent = "permanent"
  foster_home = "foster_home"

class BaseAdoption(GlobalBaseSQLModel):
  register_date: date
  kind: AdoptionKind
  revocation_date: date | None = Field(default=None)

class Adoption(BaseAdoption, table=True):
  person_id: int | None = Field(default=None, foreign_key="person.id", primary_key=True)
  animal_id: int | None = Field(default=None, foreign_key="animal.id", primary_key=True)

  person: "Person" = Relationship(back_populates="adoptions")
  animal: "Animal" = Relationship(back_populates="adopters")

  