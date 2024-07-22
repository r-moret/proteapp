from proteapp.models.adoptions import AdoptionKind
from proteapp.models.globals import GlobalBaseSQLModel
from pydantic import BaseModel
from datetime import date
from proteapp.models.adoptions import BaseAdoption

class ListedAdoption(GlobalBaseSQLModel):
    class Animal(GlobalBaseSQLModel):
        id: int
        name: str
        image: str | None = None

    class Person(GlobalBaseSQLModel):
        id: int
        name: str
        first_surname: str

    register_date: date
    kind: AdoptionKind
    revocation_date: date | None = None
    animal: Animal
    person: Person



class PublicAdoption(BaseAdoption):
    person: "PublicPerson"
    animal: "PublicAnimal"


from proteapp.api.people.schemas import PublicPerson # noqa: E402
from proteapp.api.animals.schemas import PublicAnimal # noqa: E402
PublicAdoption.model_rebuild()

