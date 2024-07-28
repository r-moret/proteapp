from enum import StrEnum
from datetime import date
from typing import TYPE_CHECKING
from proteapp.models.base import SQLAlchemyULIDType, SQLULIDSchema
from sqlmodel import Field, Relationship
from ulid import ULID

if TYPE_CHECKING:
    from proteapp.models.sql.animals import Animal
    from proteapp.models.sql.people import Person
    from proteapp.models.sql.monitorings import Monitoring


class AdoptionKind(StrEnum):
    permanent = "permanent"
    foster_home = "foster_home"


class Adoption(SQLULIDSchema, table=True):
    register_date: date
    kind: AdoptionKind
    revocation_date: date | None = Field(default=None)

    person_id: ULID = Field(
        default=None,
        foreign_key="person.id",
        primary_key=False,
        sa_type=SQLAlchemyULIDType,
    )
    animal_id: ULID = Field(
        default=None,
        foreign_key="animal.id",
        primary_key=False,
        sa_type=SQLAlchemyULIDType,
    )

    person: "Person" = Relationship(back_populates="adoptions")
    animal: "Animal" = Relationship(back_populates="adopters")
    monitorings: list["Monitoring"] = Relationship(back_populates="adoption")
