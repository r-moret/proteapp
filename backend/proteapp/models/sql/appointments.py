from sqlmodel import Field, Relationship
from proteapp.models.base import SQLULIDSchema, SQLAlchemyULIDType
from pydantic import computed_field
from typing import TYPE_CHECKING
from datetime import datetime
from ulid import ULID

if TYPE_CHECKING:
    from proteapp.models.sql.animals import Animal


class Appointment(SQLULIDSchema, table=True):
    date: datetime
    description: str

    @computed_field
    @property
    def is_past(self) -> bool:
        return self.date < datetime.now()

    animal_id: ULID = Field(default=None, foreign_key="animal.id", sa_type=SQLAlchemyULIDType)

    animal: "Animal" = Relationship(back_populates="appointments")
