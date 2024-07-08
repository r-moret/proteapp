from proteapp.models.yards import BaseYard


class CreateYard(BaseYard): ...


class UpdateYard(BaseYard): ...


class PublicYard(BaseYard):
    id: int


class PublicYardWithRelationships(PublicYard):
    animals: list["PublicAnimal"] = []


from proteapp.api.animals.schemas import PublicAnimal  # noqa: E402

PublicYardWithRelationships.model_rebuild()
