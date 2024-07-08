from fastapi import FastAPI
from proteapp.api.animals.routes import router as animals_router
from proteapp.api.treatments.routes import router as treatments_router
from proteapp.api.appointments.routes import router as appointment_router
from proteapp.database_init import init_database_data

init_database_data()

app = FastAPI()

app.include_router(animals_router)
app.include_router(treatments_router)
app.include_router(appointment_router)
