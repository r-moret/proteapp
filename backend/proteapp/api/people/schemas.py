from proteapp.models.people import BasePerson

class CreatePerson(BasePerson): ...

class UpdatePerson(BasePerson): ...

class PublicPerson(BasePerson):
  id: int

class PublicPersonWithRelationships(PublicPerson):
    user: "PublicUser" = None

from proteapp.api.users.schemas import PublicUser # noqa: E402

PublicPersonWithRelationships.model_rebuild()