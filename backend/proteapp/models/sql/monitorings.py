from datetime import date
from typing import TYPE_CHECKING
from proteapp.models.base import SQLAlchemyULIDType, SQLULIDSchema
from sqlmodel import Field, Relationship
from ulid import ULID

if TYPE_CHECKING:
    from proteapp.models.sql.adoptions import Adoption


class Monitoring(SQLULIDSchema, table=True):
    follow_date: date
    note: str

    adoption_id: ULID = Field(default=None, foreign_key="adoption.id", sa_type=SQLAlchemyULIDType)
    adoption: "Adoption" = Relationship(back_populates="monitorings")
