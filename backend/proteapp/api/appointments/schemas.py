from proteapp.models.base import ULIDSchema, BaseSchema
from datetime import datetime
from ulid import ULID


class EditableAppointment(BaseSchema):
    date: datetime
    description: str
    animal: ULID


class CompleteAppointment(ULIDSchema):
    class Animal(ULIDSchema):
        name: str

    date: datetime
    description: str
    is_past: bool
    animal: Animal
