from sqlmodel import SQLModel
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class GlobalBaseSQLModel(SQLModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)  # type: ignore
