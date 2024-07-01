from fastapi import FastAPI
from proteapp.api.routes.animals import router as animals_router
from proteapp.api.routes.treatments import router as treatments_router
from proteapp.database.mocks import init_database_data

init_database_data()

app = FastAPI()

app.include_router(animals_router)
app.include_router(treatments_router)
