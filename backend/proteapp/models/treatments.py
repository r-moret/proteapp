from sqlmodel import SQLModel, Field, Relationship


class BaseTreatment(SQLModel):
    name: str
    zone: str | None = Field(default=None)
    frequency: int | None = Field(default=None)


class BaseTreatmentWithRelationshipIds(BaseTreatment):
    animal_id: int = Field(default=None, foreign_key="animal.id")


class Treatment(BaseTreatmentWithRelationshipIds, table=True):
    id: int | None = Field(default=None, primary_key=True)

    animal: "Animal" = Relationship(back_populates="treatments")


class PublicTreatment(BaseTreatment):
    id: int


class PublicTreatmentWithAnimal(PublicTreatment):
    animal: "PublicAnimal"


class CreateTreatment(BaseTreatmentWithRelationshipIds): ...


from proteapp.models.animals import PublicAnimal, Animal  # noqa: E402

PublicTreatmentWithAnimal.model_rebuild()
