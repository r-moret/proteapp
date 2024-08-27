from typing import TYPE_CHECKING
from proteapp.models.base import SQLULIDSchema, SQLAlchemyULIDType
from sqlmodel import Field, Relationship
from ulid import ULID

if TYPE_CHECKING:
    from proteapp.models.sql.people import Person


class User(SQLULIDSchema, table=True):
    hashed_password: str | None = Field(default=None, nullable=False)
    active: bool
    veteran: bool
    image: str | None = None

    person_id: ULID = Field(
        default=None,
        foreign_key="person.id",
        unique=True,
        sa_type=SQLAlchemyULIDType,
    )

    person: "Person" = Relationship(back_populates="user")
