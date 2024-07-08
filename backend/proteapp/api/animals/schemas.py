from proteapp.models.animals import BaseAnimal


class CreateAnimal(BaseAnimal): ...


class UpdateAnimal(BaseAnimal): ...


class PublicAnimal(BaseAnimal):
    id: int


class PublicAnimalWithRelationships(PublicAnimal):
    treatments: list["PublicTreatment"] = []
    yard: "PublicYard | None" = None


from proteapp.api.treatments.schemas import PublicTreatment  # noqa: E402
from proteapp.api.yards.schemas import PublicYard  # noqa: E402

PublicAnimalWithRelationships.model_rebuild()
