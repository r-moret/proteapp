from typing import TYPE_CHECKING
from proteapp.models.globals import GlobalBaseSQLModel
from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    from proteapp.models.people import Person

class BaseUser(GlobalBaseSQLModel):
  password: str
  active: bool

  person_id: int = Field(default=None, foreign_key="person.id")

class User(BaseUser, table=True):
   id: int | None = Field(default=None, primary_key=True)

   person: "Person" = Relationship(back_populates="user")