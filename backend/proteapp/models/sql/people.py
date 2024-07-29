from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from proteapp.models.base import SQLULIDSchema
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional

if TYPE_CHECKING:
    from proteapp.models.sql.users import User
    from proteapp.models.sql.adoptions import Adoption

PhoneNumber.phone_format = "E164"


class Person(SQLULIDSchema, table=True):
    name: str
    first_surname: str
    email: str
    phone: PhoneNumber
    second_surname: str | None = Field(default=None)

    user: Optional["User"] = Relationship(back_populates="person")
    adoptions: list["Adoption"] = Relationship(back_populates="person")
