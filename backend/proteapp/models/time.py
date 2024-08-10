from pydantic import field_validator, field_serializer
from proteapp.models.base import BaseSchema
from typing import Any
from datetime import datetime, time, timezone


class UTCSchema(BaseSchema):
    @field_validator("*")
    @classmethod
    def utc_convert(cls, value: Any):
        if not isinstance(value, (datetime, time)):
            return value

        if value.tzinfo is None:
            raise ValueError("All times passed must contain timezone info (tzinfo was None)")

        if isinstance(value, datetime):
            return value.astimezone(timezone.utc)
        else:
            return datetime.combine(datetime.now(), value).astimezone(timezone.utc).timetz()

    @field_serializer("*")
    def utc_serialize(self, value: Any):
        if not isinstance(value, time):
            return value

        return value.strftime("%H:%M:%S%:z")
