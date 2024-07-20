from proteapp.api.treatments.schemas import EditableTreatment
from proteapp.models.sql.treatments import Treatment
from sqlmodel import Session
from proteapp.api.deps import sql_engine
from proteapp.models.sql.animals import Animal


def to_treatment(data: EditableTreatment) -> Treatment:
    with Session(sql_engine) as session:
        return Treatment.model_validate(
            {
                **data.model_dump(),
                "animal_id": (
                    animal.id
                    if data.animal and (animal := session.get(Animal, data.animal))
                    else None
                ),
            }
        )
