from fastapi import FastAPI
from proteapp.api.routes.animals import router as animals_router
from proteapp.api.deps import get_session
from proteapp.models.animals import Animal, Sex
from proteapp.models.treatments import Treatment


def main():
    session_generator = get_session()
    session = next(session_generator)

    animal = Animal(name="Juan", sex=Sex.male)

    treatment = Treatment(name="Paracetamol", animal=animal)

    session.add(treatment)
    session.commit()
    session.refresh(animal)

    session.close()


main()

app = FastAPI()

app.include_router(animals_router)
