from proteapp.models.base import ULIDSchema, BaseSchema
from datetime import date, datetime
from ulid import ULID


class EditableMonitoring(BaseSchema):
    follow_date: date | datetime
    note: str
    adoption: ULID


class CompleteMonitoring(ULIDSchema):
    class Adoption(ULIDSchema): ...

    follow_date: date | datetime
    note: str
    adoption: Adoption
