from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.pool import StaticPool

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
