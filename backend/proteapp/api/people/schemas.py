from proteapp.models.base import ULIDSchema, BaseSchema


class EditablePerson(BaseSchema):
    name: str
    first_surname: str
    email: str
    phone: str
    second_surname: str | None = None


class ListedPerson(ULIDSchema):
    name: str
    first_surname: str
    email: str
    second_surname: str | None


class CompletePerson(ULIDSchema):
    name: str
    first_surname: str
    email: str
    phone: str
    second_surname: str | None
