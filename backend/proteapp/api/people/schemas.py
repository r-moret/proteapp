from proteapp.models.people import BasePerson

class CreatePerson(BasePerson): ...

class UpdatePerson(BasePerson): ...

class PublicPerson(BasePerson):
  id: int

class PublicPersonWithRelationships(PublicPerson):
    user: "PublicUser" = None
    adoptions: list["PublicAdoption"] = []

from proteapp.api.users.schemas import PublicUser # noqa: E402
from proteapp.api.adoptions.schemas import PublicAdoption # noqa: E402
from proteapp.api.animals.schemas import PublicAnimal

PublicPersonWithRelationships.model_rebuild()