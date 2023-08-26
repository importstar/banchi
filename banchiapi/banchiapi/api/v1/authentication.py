from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)

import typing

from banchiapi import models
from banchiapi.core import security, deps
from banchiapi.core.config import settings
from banchiapi import schemas
import datetime

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/token",
    summary="Get OAuth2 access token",
)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    basic_credentials: typing.Optional[HTTPBasicCredentials] = Depends(
        deps.reusable_oauth2
    ),
) -> schemas.users.Token:
    failed_auth = HTTPException(
        status_code=400, detail="Incorrect username or password"
    )

    if form_data.client_id and form_data.client_secret:
        client_id = form_data.client_id
        client_secret = form_data.client_secret
    elif basic_credentials:
        client_id = basic_credentials.username
        client_secret = basic_credentials.password
    else:
        raise failed_auth

    api_client = get_api_client_by_id(db, client_id)
    if not api_client or not api_client.enabled:
        raise failed_auth
    if not verify_password(client_secret, api_client.hashed_secret):
        raise failed_auth

    access_token = create_access_token(
        data={"sub": f"api_client:{client_id}"}, **token_settings
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(token_settings["expires_delta"].total_seconds()),
    }


@router.post(
    "/login",
)
async def authentication(
    form_data: OAuth2PasswordRequestForm = Depends(),
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
    return schemas.users.Token(
        access_token=security.create_access_token(
            str(user.id),
            data={"issued_at": int(round(user.last_login_date.timestamp() * 1000))},
        ),
        refresh_token=security.create_refresh_token(
            str(user.id),
            data={"issued_at": int(round(user.last_login_date.timestamp() * 1000))},
        ),
        token_type="Bearer",
        scope="",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires_at=datetime.datetime.now()
        + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        issued_at=user.last_login_date,
    )


@router.get("/refresh_token")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    refresh_token = credentials.credentials

    jwt_handler = get_jwt_handler()
    new_token = jwt_handler.refresh_token(refresh_token)
    return {"access_token": new_token}
