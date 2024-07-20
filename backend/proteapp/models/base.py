from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import Field as SQLField, SQLModel
from sqlalchemy.types import String, TypeDecorator
from sqlalchemy.engine import Dialect
from ulid import ULID
from beanie import Document


class BaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)  # type: ignore


class ULIDSchema(BaseSchema):
    id: ULID


class SQLAlchemyULIDType(TypeDecorator[ULID]):
    impl = String

    cache_ok = True

    def process_bind_param(self, value: ULID | None, dialect: Dialect) -> str | None:
        return value if value is None else str(value)

    def process_result_value(self, value: str | None, dialect: Dialect) -> ULID | None:
        return value if value is None else ULID.from_str(value)


class SQLULIDSchema(ULIDSchema, SQLModel):
    id: ULID = SQLField(default_factory=ULID, primary_key=True, sa_type=SQLAlchemyULIDType)


class NoSQLULIDSchema(ULIDSchema, Document):
    id: ULID = Field(default_factory=ULID)

    class Settings:
        validate_on_save = True
        bson_encoders = {ULID: str}
