from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.pool import StaticPool
from odmantic import SyncEngine

# These imports are mandatory to ensure that once the SQL database
# is created, all models are registered
from proteapp.models.animals import Animal  # noqa: F401
from proteapp.models.appointments import Appointment  # noqa: F401
from proteapp.models.treatments import Treatment  # noqa: F401
from proteapp.models.yards import Yard  # noqa: F401
from proteapp.models.people import Person  # noqa: F401
from proteapp.models.users import User  # noqa: F401

sql_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SQLModel.metadata.create_all(sql_engine)

nosql_engine = SyncEngine()


def get_sql_session():
    with Session(sql_engine) as session:
        yield session


def get_nosql_session():
    with nosql_engine.session() as session:
        yield session
