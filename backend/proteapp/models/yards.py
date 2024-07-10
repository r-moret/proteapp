from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from proteapp.models.animals import Animal


class BaseYard(SQLModel):
    name: str


class Yard(BaseYard, table=True):
    id: int | None = Field(default=None, primary_key=True)

    animals: list["Animal"] = Relationship(back_populates="yard")
