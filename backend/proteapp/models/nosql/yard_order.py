from proteapp.models.base import NoSQLULIDSchema
from proteapp.models.base import ULIDSchema
from datetime import datetime


class YardOrder(NoSQLULIDSchema):
    class Yard(ULIDSchema):
        name: str

    yard_order: list[Yard]
    date: datetime
