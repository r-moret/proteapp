from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.pool import StaticPool

from proteapp.models.animals import Animal
from proteapp.models.appointments import Appointment
from proteapp.models.treatments import Treatment
from proteapp.models.yards import Yard
from proteapp.models.people import Person
from proteapp.models.users import User

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
