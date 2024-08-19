import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from proteapp.api.auth.schemas import TokenData
import os
from fastapi import HTTPException, status


def create_token(user_id: str):
    data = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
    }

    return jwt.encode(data, os.environ["JWT_SECRET_KEY"], algorithm=os.environ["JWT_ALGORITHM"])


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token, os.environ["JWT_SECRET_KEY"], algorithms=[os.environ["JWT_ALGORITHM"]]
        )
        user_id: str | None = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenData(user_id=user_id)
