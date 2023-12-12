from fastapi import Depends, HTTPException, status, Path, Query
from fastapi.security import OAuth2PasswordBearer

import typing
from jose import jwt
from pydantic import ValidationError

from loguru import logger

from beanie import PydanticObjectId
from beanie.odm.operators.find import comparison

from .. import models
from .. import schemas
from . import security


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


async def get_current_user(
    token: typing.Annotated[str, Depends(oauth2_scheme)]
) -> models.users.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.users.TokenData(user_id=user_id)
    except jwt.JWTError:
        raise credentials_exception

    # user = get_user(fake_users_db, username=token_data.username)
    user = await models.users.User.get(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: typing.Annotated[models.users.User, Depends(get_current_user)]
    # current_user: models.users.User = Depends(get_current_user),
) -> models.users.User:
    if current_user.status != "active":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: typing.Annotated[models.users.User, Depends(get_current_user)],
) -> models.users.User:
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


async def get_current_user_spaces(
    user: typing.Annotated[models.users.User, Depends(get_current_user)]
) -> list[models.spaces.Space]:
    space_roles = await models.spaces.SpaceRole.find(
        models.spaces.SpaceRole.member.id == user.id,
        models.spaces.SpaceRole.status == "active",
        fetch_links=True,
    ).to_list()

    spaces = await models.spaces.Space.find(
        comparison.In(
            models.spaces.Space.id, [space_role.space.id for space_role in space_roles]
        ),
        models.spaces.Space.status == "active",
        fetch_links=True,
    ).to_list()

    return spaces


async def get_current_user_space(
    space_id: typing.Annotated[PydanticObjectId, Path()],
    user: typing.Annotated[models.users.User, Depends(get_current_user)],
) -> models.spaces.Space:
    db_space_role = await models.spaces.SpaceRole.find_one(
        models.spaces.SpaceRole.member.id == user.id,
        models.spaces.SpaceRole.space.id == space_id,
        models.spaces.SpaceRole.status == "active",
        fetch_links=True,
    )

    if not db_space_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this space role",
        )

    return db_space_role.space


async def get_account_by_space(
    space: typing.Annotated[models.spaces.Space, Depends(get_current_user_space)],
) -> models.accounts.Account:
    db_account = await models.accounts.Account.find_one(
        models.accounts.Account.space.id == space.id,
        models.accounts.Account.status == "active",
        fetch_links=True,
    )
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this account",
        )

    return db_account


async def get_account(
    account_id: typing.Annotated[PydanticObjectId, Query()],
    user: typing.Annotated[models.users.User, Depends(get_current_user)],
) -> models.accounts.Account:
    db_account = await models.accounts.Account.find_one(
        models.accounts.Account.id == account_id,
        models.accounts.Account.status == "active",
        fetch_links=True,
    )

    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found account books",
        )

    db_space_role = await models.spaces.SpaceRole.find_one(
        models.spaces.SpaceRole.space.id == db_account.space.id,
        models.spaces.SpaceRole.member.id == user.id,
        models.spaces.SpaceRole.status == "active",
        fetch_links=True,
    )

    if not db_space_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found space role",
        )

    return db_account


async def get_account_books_by_account(
    account: typing.Annotated[models.accounts.Account, Depends(get_account)],
) -> list[models.account_books.AccountBook]:
    db_account_books = await models.account_books.AccountBook.find(
        models.account_books.AccountBook.account.id == account.id,
        models.account_books.AccountBook.status == "active",
        fetch_links=True,
    ).to_list()
    if not db_account_books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found account books",
        )

    return db_account_books


async def get_account_book(
    account_book_id: typing.Annotated[PydanticObjectId, Path()],
    user: typing.Annotated[models.users.User, Depends(get_current_user)],
) -> models.account_books.AccountBook:
    db_account_book = await models.account_books.AccountBook.find_one(
        models.account_books.AccountBook.id == account_book_id,
        models.account_books.AccountBook.status == "active",
        fetch_links=True,
    )

    db_account = await get_account(db_account_book.account.id, user)

    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found account",
        )

    return db_account_book


async def get_transaction(
    transaction_id: typing.Annotated[PydanticObjectId, Path()],
    user: typing.Annotated[models.users.User, Depends(get_current_user)],
) -> models.account_books.AccountBook:
    db_transaction = await models.transactions.Transaction.find_one(
        models.transactions.Transaction.id == transaction_id, fetch_links=True
    )

    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found transaction",
        )

    db_account_book = await get_account_book(db_transaction.from_account_book.id, user)

    if not db_account_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found account book",
        )

    return db_transaction


async def create_logs(action, request, current_user):
    request_log = models.RequestLog(
        user=current_user,
        ip_address=request.client.host,
        action=action,
        user_agent=request.headers.get("user-agent", ""),
    )
    return request_log


class RoleChecker:
    def __init__(self, *allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        user: typing.Annotated[models.users.User, Depends(get_current_active_user)],
    ):
        for role in user.roles:
            if role in self.allowed_roles:
                return
        logger.debug(f"User with role {user.roles} not in {self.allowed_roles}")
        raise HTTPException(status_code=403, detail="Role not permitted")


class DivisionChecker:
    def __init__(self, *allowed_divisions: list[str]):
        self.allowed_divisions = allowed_divisions

    def __call__(
        self,
        user: typing.Annotated[models.users.User, Depends(get_current_active_user)],
    ):
        if user.division not in self.allowed_divisions:
            logger.debug(
                f"User with division {user.division} not in {self.allowed_divisions}"
            )
            raise HTTPException(status_code=403, detail="Division not permitted")
