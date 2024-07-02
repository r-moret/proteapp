from proteapp.models.treatments import BaseTreatment


class CreateTreatment(BaseTreatment): ...


class PublicTreatment(BaseTreatment):
    id: int
