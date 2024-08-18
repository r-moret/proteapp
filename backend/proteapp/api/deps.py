from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.pool import StaticPool
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

# These imports are mandatory to ensure that once the SQL database
# is created, all models are registered
from proteapp.models.sql.animals import Animal  # noqa: F401
from proteapp.models.sql.appointments import Appointment  # noqa: F401
from proteapp.models.sql.treatments import Treatment  # noqa: F401
from proteapp.models.sql.yards import Yard  # noqa: F401
from proteapp.models.sql.people import Person  # noqa: F401
from proteapp.models.sql.users import User  # noqa: F401
from proteapp.models.sql.adoptions import Adoption  # noqa: F401
from proteapp.models.sql.monitorings import Monitoring  # noqa: F401

from proteapp.models.nosql.inform import Inform
from proteapp.models.nosql.shift import Shift, TimeTable, DayTime


async def connect_mongo():
    nosql_client = AsyncIOMotorClient()
    await init_beanie(database=nosql_client.db_name, document_models=[Inform, Shift])


sql_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SQLModel.metadata.create_all(sql_engine)


def get_sql_session():
    with Session(sql_engine) as session:
        yield session


async def init_shift():
    shift = await Shift.find_one()

    if not shift:
        shift = Shift(
            status="open",
            timetable=TimeTable(
                monday=DayTime(morning=[], afternoon=[]),
                thursday=DayTime(morning=[], afternoon=[]),
                wednesday=DayTime(morning=[], afternoon=[]),
                tuesday=DayTime(morning=[], afternoon=[]),
                friday=DayTime(morning=[], afternoon=[]),
                saturday=DayTime(morning=[], afternoon=[]),
                sunday=DayTime(morning=[], afternoon=[]),
            ),
        )

        await shift.save()
