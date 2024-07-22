from proteapp.models.base import ULIDSchema, BaseSchema


class EditableYard(BaseSchema):
    name: str


class ListedYard(ULIDSchema):
    name: str


class CompleteYard(ListedYard):
    class Animal(ULIDSchema):
        name: str

    animals: list[Animal]
