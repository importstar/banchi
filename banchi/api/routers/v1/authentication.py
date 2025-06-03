from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)

import typing
import bson

from banchi.api import models
from banchi.api.core import security, deps
from banchi.api.core.config import settings
from banchi.api import schemas
import datetime

router = APIRouter(prefix="/auth", tags=["authentication"])



@router.post(
    "/login",
)
async def authentication(
    form_data: typing.Annotated[OAuth2PasswordRequestForm, Depends()],
    name="auth:login",
) -> schemas.users.Token:
    user = await models.users.User.find_one(
        models.users.User.username == form_data.username
    )

    if not user:
        user = await models.users.User.find_one(
            models.users.User.email == form_data.username
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not await user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    user.last_login_date = datetime.datetime.now()
    await user.save()
    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token_expires = datetime.timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    return schemas.users.Token(
        access_token=security.create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        ),
        refresh_token=security.create_refresh_token(
            data={"sub": str(user.id)}, expires_delta=refresh_token_expires
        ),
        token_type="Bearer",
        scope="",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires_at=datetime.datetime.now() + access_token_expires,
        issued_at=user.last_login_date,
    )


@router.get("/refresh")
async def refresh_token(
    credentials: typing.Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())],
)-> schemas.users.AccessToken:
    refresh_token = credentials.credentials

    data = security.verify_refresh_token(refresh_token)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id = data.get("sub")
    user = await models.User.find_one(
        models.User.id == bson.ObjectId(user_id),
         models.User.status== "active"
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    now = datetime.datetime.now()
    token = schemas.users.AccessToken(
        access_token=security.create_access_token(
            data={"sub": str(user.id)},
            expires_delta=datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
        token_type="Bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires_at=now + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        issued_at=now,
        scope=""
    )
    return token


