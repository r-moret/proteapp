from proteapp.models.sql.animals import Sex
from proteapp.models.base import ULIDSchema, BaseSchema
from datetime import date, datetime
from ulid import ULID


class EditableAnimal(BaseSchema):
    name: str
    sex: Sex
    personality: str | None = None
    description: str | None = None
    birth_date: date | None = None
    entry_date: date | None = None
    is_animal_compatible: bool | None = None
    is_castrated: bool | None = None
    image: str | None = None
    yard: ULID | None = None


class ListedAnimal(ULIDSchema):
    class Treatment(ULIDSchema):
        name: str

    class Yard(ULIDSchema):
        name: str

    name: str
    sex: Sex
    image: str | None
    yard: Yard | None
    birth_date: date | None
    is_animal_compatible: bool | None
    is_castrated: bool | None
    treatments: list[Treatment]


class CompleteAnimal(ListedAnimal):
    class Treatment(ULIDSchema):
        name: str
        zone: str | None
        frequency: int | None
        end_date: datetime | None
        amount: str | None

    class Appointment(ULIDSchema):
        date: datetime
        description: str
        is_past: bool

    personality: str | None
    description: str | None
    birth_date: date | None
    entry_date: date | None
    is_animal_compatible: bool | None
    is_castrated: bool | None
    treatments: list[Treatment]
    appointments: list[Appointment]
