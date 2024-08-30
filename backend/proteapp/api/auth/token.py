import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timezone, timedelta
from proteapp.api.auth.schemas import TokenData
import os
from pydantic import ValidationError
from fastapi.security import SecurityScopes
from proteapp.exceptions import TokenDecodificationError


def create_token(user_id: str, roles: list[str] | None = None):
    data = {
        "sub": user_id,
        "scopes": roles,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
    }

    return jwt.encode(data, os.environ["JWT_SECRET_KEY"], algorithm=os.environ["JWT_ALGORITHM"])


def decode_token(token: str, security_scopes: SecurityScopes) -> TokenData:
    try:
        payload = jwt.decode(
            token, os.environ["JWT_SECRET_KEY"], algorithms=[os.environ["JWT_ALGORITHM"]]
        )
        user_id: str | None = payload.get("sub")
        scopes: list[str] = payload.get("scopes", [])

        if not user_id:
            raise TokenDecodificationError("Could not validate credentials")

        token_data = TokenData(user_id=user_id, scopes=scopes)

        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise TokenDecodificationError("Not enough permissions")

    except (InvalidTokenError, ValidationError):
        raise TokenDecodificationError("Could not validate credentials")

    return token_data
