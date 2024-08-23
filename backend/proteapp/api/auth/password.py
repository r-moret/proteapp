from passlib.context import CryptContext
from proteapp.models.sql.users import User
from proteapp.models.sql.people import Person
from proteapp.api.deps import sql_engine
from sqlmodel import Session, select
from typing import Literal

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str) -> bool:
    return context.verify(password, hashed_password)


def hash_password(password: str) -> str:
    return context.hash(password)


def authenticate(username: str, password: str) -> User | Literal[False]:
    with Session(sql_engine) as session:
        results = session.exec(select(User).join(Person).where(Person.email == username))
        user = results.first()

        if not user or not verify_password(password, user.hashed_password):
            return False

        return user
