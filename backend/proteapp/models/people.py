from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from proteapp.models.globals import GlobalBaseSQLModel
from pydantic_extra_types.phone_numbers import PhoneNumber
from proteapp.models.adoptions import Adoption

if TYPE_CHECKING:
    from proteapp.models.users import User
    from proteapp.models.adoptions import Adoption

PhoneNumber.phone_format = 'E164'

class BasePerson(GlobalBaseSQLModel):
    name: str
    first_surname: str
    phone: PhoneNumber
    second_surname: str | None = Field(default=None)
    email: str | None = Field(default=None)

class Person(BasePerson, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user: "User" = Relationship(back_populates="person")
    adoptions: list["Adoption"] = Relationship(back_populates="person")