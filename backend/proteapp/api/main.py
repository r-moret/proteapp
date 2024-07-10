from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from proteapp.api.animals.routes import router as animals_router
from proteapp.api.treatments.routes import router as treatments_router
from proteapp.api.appointments.routes import router as appointment_router
from proteapp.api.yards.routes import router as yards_router
from proteapp.database_init import init_database_data

init_database_data()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(animals_router)
app.include_router(treatments_router)
app.include_router(appointment_router)
app.include_router(yards_router)
