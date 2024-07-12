from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from proteapp.models.globals import GlobalBaseSQLModel

if TYPE_CHECKING:
    from proteapp.models.animals import Animal


class BaseYard(GlobalBaseSQLModel):
    name: str


class Yard(BaseYard, table=True):
    id: int | None = Field(default=None, primary_key=True)

    animals: list["Animal"] = Relationship(back_populates="yard")
