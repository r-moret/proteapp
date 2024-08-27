from proteapp.api.animals.schemas import EditableAnimal
from proteapp.models.sql.animals import Animal
from proteapp.models.sql.yards import Yard
from proteapp.api.deps import sql_engine
from sqlmodel import Session
from datetime import datetime


def to_animal(data: EditableAnimal) -> Animal:
    with Session(sql_engine) as session:
        return Animal.model_validate(
            {
                **data.model_dump(),
                "birth_date": data.birth_date
                if not isinstance(data.birth_date, datetime)
                else data.birth_date.date(),
                "entry_date": data.entry_date
                if not isinstance(data.entry_date, datetime)
                else data.entry_date.date(),
                "yard_id": (
                    Yard.model_validate(
                        animal_yard.model_dump()  # type: ignore
                        if (animal_yard := session.get(Yard, data.yard))
                        else None
                    ).id
                    if data.yard
                    else None
                ),
            }
        )
