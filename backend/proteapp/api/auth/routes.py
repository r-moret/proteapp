from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from proteapp.api.auth.password import authenticate
from proteapp.api.auth.token import create_token
from proteapp.api.auth.schemas import Token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
def generate_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_token(str(user.id), [user.role])
    return Token(access_token=token, token_type="bearer")
