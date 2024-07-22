from sqlmodel import Relationship
from typing import TYPE_CHECKING
from proteapp.models.base import SQLULIDSchema

if TYPE_CHECKING:
    from proteapp.models.sql.animals import Animal


class Yard(SQLULIDSchema, table=True):
    name: str

    animals: list["Animal"] = Relationship(back_populates="yard")
