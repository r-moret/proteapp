from proteapp.api.adoptions.schemas import EditableAdoption
from proteapp.models.sql.adoptions import Adoption
from proteapp.models.sql.animals import Animal
from proteapp.models.sql.people import Person
from proteapp.api.deps import sql_engine
from sqlmodel import Session
from proteapp.exceptions import UnsavedDataError


def to_adoption(data: EditableAdoption) -> Adoption:
    with Session(sql_engine) as session:
        adoption_animal = session.get(Animal, data.animal)
        adoption_person = session.get(Person, data.person)

        if not adoption_animal:
            raise UnsavedDataError(
                "Cannot create an adoption with an animal that doesn't exist",
                field="animal",
            )
        if not adoption_person:
            raise UnsavedDataError(
                "Cannot create an adoption with a person that doesn't exist",
                field="person",
            )

        return Adoption.model_validate(
            {**dict(data), "animal_id": adoption_animal.id, "person_id": adoption_person.id}
        )
