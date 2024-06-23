from fastapi import FastAPI
from proteapp.api.routes.animals import router as animals_router

app = FastAPI()

app.include_router(animals_router)

