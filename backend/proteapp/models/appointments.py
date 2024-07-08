from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Tuple
from datetime import datetime

if TYPE_CHECKING:
    from proteapp.models.animals import Animal


class BaseAppointment(SQLModel):
    date: datetime
    description: str | None = Field(default=None)
    
    animal_id: int = Field(default=None, foreign_key="animal.id")


class Appointment(BaseAppointment, table=True):
    id: int | None = Field(default=None, primary_key=True)

    animal: "Animal" = Relationship(back_populates="appointment")
