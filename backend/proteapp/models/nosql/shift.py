from proteapp.models.base import NoSQLULIDSchema, BaseSchema
from typing import Literal
from ulid import ULID
from pydantic import field_serializer


class DayTime(BaseSchema):
    morning: list[ULID]
    afternoon: list[ULID]

    @field_serializer("morning", "afternoon")
    def serialize_ulid(self, value: list[ULID]):
        return [str(id) for id in value]


class TimeTable(BaseSchema):
    monday: DayTime
    thursday: DayTime
    wednesday: DayTime
    tuesday: DayTime
    friday: DayTime
    saturday: DayTime
    sunday: DayTime


class Shift(NoSQLULIDSchema):
    status: Literal["open", "closed"]
    timetable: TimeTable
