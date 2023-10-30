import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status

from loguru import logger

import bson

from banchiapi import models
from banchiapi.core import deps
from banchiapi import schemas

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get(
    "",
    response_model_by_alias=False,
)
async def get_all(
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.accounts.AccountList:
    db_accounts = await models.accounts.Account.find(
        models.accounts.Account.creator == current_user
    ).to_list()
    return dict(accounts=db_accounts)


@router.post(
    "/create",
    response_model_by_alias=False,
)
async def create(
    account: schemas.accounts.CreatedAccount,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.accounts.Account:
    db_space = models.spaces.Space.find_one(
        models.spaces.Space.id == bson.ObjectId(account.space_id),
        models.spaces.Space.owner == current_user,
    )

    if db_space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Space id {account.space_id} not found",
        )

    data = account.dict()
    db_account = models.Account(**data)
    db_account.creator = current_user
    db_account.space = db_space
    db_account.created_date = datetime.datetime.now()
    db_account.updated_date = datetime.datetime.now()
    db_account.save()

    return db_account


@router.get(
    "/{account_id}",
    response_model_by_alias=False,
)
def get(
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
    return db_account


@router.put(
    "/{account_id}/update",
    response_model_by_alias=False,
    response_model=schemas.accounts.Account,
)
def update(
    account_id: str,
    account: schemas.accounts.CreatedAccount,
    current_user: models.users.User = Depends(deps.get_current_user),
):
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
    "/{account_id}/delete",
    response_model_by_alias=False,
    response_model=schemas.accounts.Account,
)
def delete_account(
    account_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
):
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
