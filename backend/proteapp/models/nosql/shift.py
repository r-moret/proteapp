from proteapp.models.base import NoSQLULIDSchema, BaseSchema
from typing import Literal
from ulid import ULID


class DayTime(BaseSchema):
    morning: list[ULID]
    afternoon: list[ULID]


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
