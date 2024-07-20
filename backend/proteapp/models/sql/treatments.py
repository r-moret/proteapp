from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from datetime import datetime
from proteapp.models.base import SQLULIDSchema, SQLAlchemyULIDType
from ulid import ULID

if TYPE_CHECKING:
    from proteapp.models.sql.animals import Animal


class Treatment(SQLULIDSchema, table=True):
    name: str
    zone: str | None = Field(default=None)
    frequency: int | None = Field(default=None)
    end_date: datetime | None = Field(default=None)
    amount: str | None = Field(default=None)

    animal_id: ULID = Field(default=None, foreign_key="animal.id", sa_type=SQLAlchemyULIDType)

    animal: "Animal" = Relationship(back_populates="treatments")
