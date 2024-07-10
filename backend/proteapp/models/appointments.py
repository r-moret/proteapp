from sqlmodel import SQLModel, Field, Relationship
from pydantic import computed_field
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from proteapp.models.animals import Animal


class BaseAppointment(SQLModel):
    date: datetime
    description: str | None = Field(default=None)

    @computed_field
    @property
    def is_past(self) -> bool:
        return self.date < datetime.now()

    animal_id: int = Field(default=None, foreign_key="animal.id")


class Appointment(BaseAppointment, table=True):
    id: int | None = Field(default=None, primary_key=True)

    animal: "Animal" = Relationship(back_populates="appointments")
