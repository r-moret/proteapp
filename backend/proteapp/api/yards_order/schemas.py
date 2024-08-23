from proteapp.api.yards.schemas import ListedYard
from proteapp.models.base import ULIDSchema, BaseSchema
from datetime import datetime

from ulid import ULID


class ListedYardOrder(ULIDSchema):
    date: datetime
    yard_order: list[ListedYard]


class EditableYardOrder(BaseSchema):
    date: datetime
    yard_order: list[ULID]
