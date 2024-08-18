from proteapp.models.base import BaseSchema
from proteapp.models.nosql.shift import TimeTable
from typing import Literal
from ulid import ULID
from enum import StrEnum


class ShiftStatus(BaseSchema):
    status: Literal["open", "closed"]


class ShiftData(BaseSchema):
    connected: int
    timetable: TimeTable


class ShiftAction(BaseSchema):
    class ActionType(StrEnum):
        ADD_USER = "add_user"
        REMOVE_USER = "remove_user"

    class Selection(BaseSchema):
        day: Literal["monday", "thursday", "wednesday", "tuesday", "friday", "saturday", "sunday"]
        time: Literal["morning", "afternoon"]

    type: ActionType
    user: ULID
    shift: Selection
