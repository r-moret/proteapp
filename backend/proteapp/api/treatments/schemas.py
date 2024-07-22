from proteapp.models.base import ULIDSchema, BaseSchema
from datetime import datetime
from ulid import ULID


class EditableTreatment(BaseSchema):
    name: str
    zone: str | None = None
    frequency: int | None = None
    end_date: datetime | None = None
    amount: str | None = None
    animal: ULID


class CompleteTreatment(ULIDSchema):
    class Animal(ULIDSchema):
        name: str

    name: str
    zone: str | None
    frequency: int | None
    end_date: datetime | None
    amount: str | None
    animal: Animal
