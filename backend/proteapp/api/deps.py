from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.pool import StaticPool
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.security import OAuth2PasswordBearer
from fastapi import UploadFile
from typing import Annotated
from fastapi import Depends, HTTPException, status, Query, WebSocketException, Security
from fastapi.security import SecurityScopes
from pathlib import Path
from ulid import ULID
import os
import shutil

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
from proteapp.models.nosql.yard_order import YardOrder

from proteapp.api.auth.token import decode_token
from proteapp.exceptions import TokenDecodificationError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def connect_mongo():
    nosql_client = AsyncIOMotorClient()
    await init_beanie(database=nosql_client.db_name, document_models=[Inform, Shift, YardOrder])


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


def get_logged_user_http(
    token: Annotated[str, Depends(oauth2_scheme)], security_scopes: SecurityScopes
) -> User:
    auth_header = (
        "Bearer" + "" if not security_scopes.scopes else f' scope="{security_scopes.scope_str}"'
    )

    try:
        token_data = decode_token(token, security_scopes)
    except TokenDecodificationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": auth_header},
        )

    with Session(sql_engine) as session:
        user = session.get(User, token_data.user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": auth_header},
            )

    return user


def get_logged_user_ws(token: Annotated[str, Query()], security_scopes: SecurityScopes):
    try:
        token_data = decode_token(token, security_scopes)
    except TokenDecodificationError as e:
        raise WebSocketException(
            code=status.WS_1003_UNSUPPORTED_DATA,
            reason=str(e),
        )

    with Session(sql_engine) as session:
        user = session.get(User, token_data.user_id)

        if not user:
            raise WebSocketException(
                code=status.WS_1003_UNSUPPORTED_DATA,
                reason="Could not validate credentials",
            )

    return user


def admin_required(user: Annotated[User, Security(get_logged_user_http, scopes=["admin"])]): ...


def save_image(image: UploadFile) -> str:
    if not image.filename:
        raise HTTPException(422, "Unable to upload an image with no filename")

    image_new_filename = f"{ULID()}{Path(image.filename).suffix}"
    image_path = f"images/{image_new_filename}"

    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    with open(image_path, "wb") as file:
        shutil.copyfileobj(image.file, file)

    return image_path
