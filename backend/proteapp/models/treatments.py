from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from datetime import datetime
from proteapp.models.globals import GlobalBaseSQLModel

if TYPE_CHECKING:
    from proteapp.models.animals import Animal


class BaseTreatment(GlobalBaseSQLModel):
    name: str
    zone: str | None = Field(default=None)
    frequency: int | None = Field(default=None)
    end_date: datetime | None = Field(default=None)
    amount: str | None = Field(default=None)

    animal_id: int = Field(default=None, foreign_key="animal.id")


class Treatment(BaseTreatment, table=True):
    id: int | None = Field(default=None, primary_key=True)

    animal: "Animal" = Relationship(back_populates="treatments")
