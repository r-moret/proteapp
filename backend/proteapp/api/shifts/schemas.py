from proteapp.models.base import BaseSchema
from typing import Literal
from ulid import ULID
from enum import StrEnum


class ShiftStatus(BaseSchema):
    status: Literal["open", "closed"]


class ShiftActionType(StrEnum):
    ADD_USER = "add_user"
    REMOVE_USER = "remove_user"


class ShiftData(BaseSchema):
    day: Literal["monday", "thursday", "wednesday", "tuesday", "friday", "saturday", "sunday"]
    time: Literal["morning", "afternoon"]


class ShiftAction(BaseSchema):
    type: ShiftActionType
    user: ULID
    shift: ShiftData
