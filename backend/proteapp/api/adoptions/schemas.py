from proteapp.models.adoptions import BaseAdoption

class PublicAdoption(BaseAdoption):
    person: "PublicPerson"
    animal: "PublicAnimal"


from proteapp.api.people.schemas import PublicPerson # noqa: E402
from proteapp.api.animals.schemas import PublicAnimal # noqa: E402
PublicAdoption.model_rebuild()
