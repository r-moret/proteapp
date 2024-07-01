from fastapi import FastAPI
from proteapp.api.routes.animals import router as animals_router
from proteapp.api.routes.treatments import router as treatments_router
from proteapp.api.deps import get_session
from proteapp.models.animals import Animal, Sex
from proteapp.models.treatments import Treatment
from proteapp.api.fakes import animales
def main():
    session_generator = get_session()
    session = next(session_generator)

    # for data in animales:
    #     animal = Animal(
    #         name=data["name"], 
    #         description=data["description"], 
    #         personality=data["personality"], 
    #         sex=data["sex"], 
    #         birthDate=data["birthDate"], 
    #         entryDate=data["entryDate"], 
    #         isCastrated=data["isCastrated"], 
    #         isAnimalCompatible=data["isAnimalCompatible"], 
    #         yard=data["yard"], 
    #         hasTreatment=data["hasTreatment"], 
    #         image=data["image"]
    #     )
    #     session.add(animal)
    #     session.commit()

    animal = Animal(name="Juan", sex=Sex.male)

    treatment = Treatment(name="Paracetamol", animal=animal)

    session.add(treatment)
    session.commit()
    session.refresh(animal)

    session.close()


main()

app = FastAPI()

app.include_router(animals_router)
app.include_router(treatments_router)
