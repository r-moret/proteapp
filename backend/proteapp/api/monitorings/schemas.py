from proteapp.models.base import ULIDSchema, BaseSchema
from datetime import date
from ulid import ULID


class EditableMonitoring(BaseSchema):
    follow_date: date
    note: str
    adoption: ULID


class CompleteMonitoring(ULIDSchema):
    class Adoption(ULIDSchema): ...

    follow_date: date
    note: str
    adoption: Adoption
