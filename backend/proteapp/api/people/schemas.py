from proteapp.models.base import ULIDSchema, BaseSchema
from pydantic_extra_types.phone_numbers import PhoneNumber


class EditablePerson(BaseSchema):
    name: str
    first_surname: str
    phone: PhoneNumber
    second_surname: str | None = None
    email: str | None = None


class CompletePerson(ULIDSchema):
    name: str
    first_surname: str
    phone: PhoneNumber
    second_surname: str | None
    email: str | None
