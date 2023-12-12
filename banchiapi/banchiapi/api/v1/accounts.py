import datetime
import io
import typing

from fastapi import APIRouter, Depends, HTTPException, Response, status

from loguru import logger

import bson
from typing import Annotated


from banchiapi import models
from banchiapi.core import deps
from banchiapi import schemas

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("")
async def get_all(
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.accounts.AccountList:
    db_accounts = await models.accounts.Account.find(
        models.accounts.Account.status == "active",
        models.accounts.Account.creator.id == current_user.id,
        fetch_links=True,
    ).to_list()

    return dict(accounts=db_accounts)


@router.post(
    "",
)
async def create(
    account: schemas.accounts.CreatedAccount,
    current_user: Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.accounts.Account:
    db_space = await models.spaces.Space.find_one(
        models.spaces.Space.id == bson.ObjectId(account.space_id),
        models.spaces.Space.owner.id == current_user.id,
    )

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


@router.get(
    "/{account_id}",
)
async def get(
    account_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.accounts.Account:
    db_account = await models.accounts.Account.find_one(
        models.accounts.Account.id == bson.ObjectId(account_id),
        models.accounts.Account.creator.id == current_user.id,
        fetch_links=True,
    )

    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this account",
        )
    return db_account


@router.put(
    "/{account_id}",
)
async def update(
    account_id: str,
    account: schemas.accounts.CreatedAccount,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.accounts.Account:
    db_account = models.Account.objects(id=account_id).first()
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    db_accounts = models.Account.objects(
        name=account.name, status="active", id__ne=account_id
    )
    if db_accounts:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already account name",
        )
    db_accounts = models.Account.objects(
        code=account.code, status="active", id__ne=account_id
    )
    if db_accounts:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already account code",
        )

    data = account.dict()
    db_account.update(**data)

    db_account.updated_date = datetime.datetime.now()
    db_account.save()
    db_account.reload()
    return db_account


@router.delete(
    "/{account_id}",
)
async def delete(
    account_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.accounts.Account:
    try:
        db_account = models.Account.objects.get(id=account_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this account",
        )
    db_account.update(status="disactive", updated_date=datetime.datetime.now())
    db_account.reload()
    db_account.save()

    divisions = models.Division.objects(account=db_account, status="active")
    for division in divisions:
        division.status = "disactive"
        division.save()
    return db_account
