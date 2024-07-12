from sqlmodel import Field, Relationship
from proteapp.models.globals import GlobalBaseSQLModel
from pydantic import computed_field
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from proteapp.models.animals import Animal


class BaseAppointment(GlobalBaseSQLModel):
    date: datetime
    description: str

    @computed_field
    @property
    def is_past(self) -> bool:
        return self.date < datetime.now()

    animal_id: int = Field(default=None, foreign_key="animal.id")


class Appointment(BaseAppointment, table=True):
    id: int | None = Field(default=None, primary_key=True)

    animal: "Animal" = Relationship(back_populates="appointments")
