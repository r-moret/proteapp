from proteapp.models.animals import BaseAnimal


class CreateAnimal(BaseAnimal): ...


class UpdateAnimal(BaseAnimal): ...


class PublicAnimal(BaseAnimal):
    id: int


class PublicAnimalWithRelationships(PublicAnimal):
    treatments: list["PublicTreatment"] = []


from proteapp.api.treatments.schemas import PublicTreatment  # noqa: E402

PublicAnimalWithRelationships.model_rebuild()
