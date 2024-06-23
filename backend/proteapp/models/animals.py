from sqlmodel import SQLModel, Field
from datetime import date
from enum import StrEnum


class Sex(StrEnum):
    male = "male"
    female = "female"


class BaseAnimal(SQLModel):
    name: str
    sex: Sex
    personality: str | None = Field(default=None)
    description: str | None = Field(default=None)
    birthDate: date | None = Field(default=None)
    entryDate: date | None = Field(default=None)
    isAnimalCompatible: bool | None = Field(default=None)
    isCastrated: bool | None = Field(default=None)
    image: str | None = Field(default=None)


class CreateAnimal(BaseAnimal): ...


class UpdateAnimal(BaseAnimal): ...


class Animal(BaseAnimal, table=True):
    id: int | None = Field(default=None, primary_key=True)


class PublicAnimal(BaseAnimal):
    id: int
