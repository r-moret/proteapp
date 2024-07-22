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

from proteapp.models.nosql.inform import Inform


async def connect_mongo():
    nosql_client = AsyncIOMotorClient()
    await init_beanie(database=nosql_client.db_name, document_models=[Inform])


sql_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SQLModel.metadata.create_all(sql_engine)


def get_sql_session():
    with Session(sql_engine) as session:
        yield session
