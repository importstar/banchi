import datetime
import io
import typing

from fastapi import APIRouter, Depends, HTTPException, Response, status

from loguru import logger

import bson
from beanie import PydanticObjectId
from beanie.operators import Inc, Set

from banchi.api import models
from banchi.api.core import deps
from banchi.api import schemas

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("")
async def get_all(
    db_accounts: typing.Annotated[
        models.accounts.Account, Depends(deps.get_current_user_accounts)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.accounts.AccountList:
    # db_accounts = await models.accounts.Account.find(
    #     models.accounts.Account.status == "active",
    #     models.accounts.Account.creator.id == current_user.id,
    #     fetch_links=True,
    # ).to_list()

    return dict(accounts=db_accounts)


@router.post("")
async def create(
    account: schemas.accounts.CreatedAccount,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.accounts.Account:
    db_space = await deps.get_current_user_space(account.space_id, current_user)

    if not db_space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Space id {account.space_id} not found",
        )

    db_account = await models.accounts.Account.find_one(
        models.accounts.Account.space.id == db_space.id
    )

    if db_account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already account in space",
        )

    data = account.dict()
    data.pop("space_id")
    data["creator"] = current_user
    data["updated_by"] = current_user
    data["space"] = db_space
    db_account = models.accounts.Account.parse_obj(data)
    await db_account.save()

    account_book_templates = [
        ("Assets", "asset"),
        ("Equity", "equity"),
        ("Expenses", "expense"),
        ("Income", "income"),
        ("Liabilities", "liability"),
    ]

    for name, type_ in account_book_templates:
        db_account_book = models.account_books.AccountBook(
            name=name,
            type=type_,
            account=db_account,
            creator=current_user,
            updated_by=current_user,
        )
        await db_account_book.save()

    return db_account


@router.get("/{account_id}")
async def get(
    account_id: PydanticObjectId,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.accounts.Account:
    db_account = await deps.get_account(account_id, current_user)
    return db_account


@router.put("/{account_id}")
async def update(
    account_id: PydanticObjectId,
    account: schemas.accounts.UpdatedAccount,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.accounts.Account:
    db_account = await deps.get_account(account_id, current_user)

    data = account.dict()
    await db_account.update(Set(data))

    db_account.updated_date = datetime.datetime.now()
    db_account.updated_by = current_user
    await db_account.save()

    return db_account


@router.delete(
    "/{account_id}",
)
async def delete(
    account_id: PydanticObjectId,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.accounts.Account:
    db_account = await deps.get_account(account_id, current_user)

    db_account.status = "delete"
    db_account.updated_date = datetime.datetime.now()
    db_account.updated_by = current_user
    await db_account.save()

    return db_account
