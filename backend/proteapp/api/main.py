from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from proteapp.api.animals.routes import router as animals_router
from proteapp.api.treatments.routes import router as treatments_router
from proteapp.api.appointments.routes import router as appointment_router
from proteapp.api.yards.routes import router as yards_router
from proteapp.api.people.routes import router as people_router
from proteapp.api.users.routes import router as users_router
from proteapp.api.informs.routes import router as informs_router
from proteapp.api.adoptions.routes import router as adoptions_router
from proteapp.api.monitorings.routes import router as monitorings_router
from proteapp.api.shifts.routes import router as shifts_router
from proteapp.api.auth.routes import router as auth_router
from proteapp.database_init import init_database_data
from proteapp.api.deps import connect_mongo, init_shift, get_logged_user
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_mongo()
    await init_database_data()
    await init_shift()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(animals_router, dependencies=[Depends(get_logged_user)])
app.include_router(treatments_router, dependencies=[Depends(get_logged_user)])
app.include_router(appointment_router, dependencies=[Depends(get_logged_user)])
app.include_router(yards_router, dependencies=[Depends(get_logged_user)])
app.include_router(people_router, dependencies=[Depends(get_logged_user)])
app.include_router(users_router, dependencies=[Depends(get_logged_user)])
app.include_router(informs_router, dependencies=[Depends(get_logged_user)])
app.include_router(adoptions_router, dependencies=[Depends(get_logged_user)])
app.include_router(monitorings_router, dependencies=[Depends(get_logged_user)])
app.include_router(shifts_router, dependencies=[Depends(get_logged_user)])
app.include_router(auth_router)
