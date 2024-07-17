from proteapp.models.animals import BaseAnimal
from proteapp.models.adoptions import BaseAdoption


class CreateAnimal(BaseAnimal): ...


class UpdateAnimal(BaseAnimal): ...


class PublicAnimal(BaseAnimal):
    id: int


class PublicAnimalWithRelationships(PublicAnimal):
    treatments: list["PublicTreatment"] = []
    appointments: list["PublicAppointment"] = []
    yard: "PublicYard | None" = None
    adopters: list["PublicAdoption"] = []


from proteapp.api.treatments.schemas import PublicTreatment  # noqa: E402
from proteapp.api.appointments.schemas import PublicAppointment  # noqa: E402
from proteapp.api.yards.schemas import PublicYard  # noqa: E402
from proteapp.api.adoptions.schemas import PublicAdoption

PublicAnimalWithRelationships.model_rebuild()
