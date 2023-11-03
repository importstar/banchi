import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status

from loguru import logger

import bson
from typing import Annotated


from banchiapi import models
from banchiapi.core import deps
from banchiapi import schemas

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get(
    "",
    response_model_by_alias=False,
)
async def get_all(
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.transactions.AccountList:
    db_transactions = await models.transactions.Account.find(
        models.transactions.Account.status == "active",
        models.transactions.Account.creator.id == current_user.id,
        fetch_links=True,
    ).to_list()

    return dict(transactions=db_transactions)


@router.post(
    "/create",
    response_model_by_alias=False,
)
async def create(
    transaction: schemas.transactions.CreatedAccount,
    current_user: Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.Account:
    db_space = await models.spaces.Space.find_one(
        models.spaces.Space.id == bson.ObjectId(transaction.space_id),
        models.spaces.Space.owner.id == current_user.id,
    )

    if not db_space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Space id {transaction.space_id} not found",
        )

    data = transaction.dict()
    data.pop("space_id")
    data["creator"] = current_user
    data["updated_by"] = current_user
    data["space"] = db_space
    db_transaction = models.transactions.Account.parse_obj(data)
    await db_transaction.save()

    return db_transaction


@router.get(
    "/{transaction_id}",
    response_model_by_alias=False,
)
async def get(
    transaction_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.transactions.Account:
    db_transaction = await models.transactions.Account.find_one(
        models.transactions.Account.id == bson.ObjectId(transaction_id),
        models.transactions.Account.creator.id == current_user.id,
        fetch_links=True,
    )

    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this transaction",
        )
    return db_transaction


@router.put(
    "/{transaction_id}/update",
    response_model_by_alias=False,
)
async def update(
    transaction_id: str,
    transaction: schemas.transactions.CreatedAccount,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.transactions.Account:
    db_transaction = models.Account.objects(id=transaction_id).first()
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    db_transactions = models.Account.objects(
        name=transaction.name, status="active", id__ne=transaction_id
    )
    if db_transactions:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already transaction name",
        )
    db_transactions = models.Account.objects(
        code=transaction.code, status="active", id__ne=transaction_id
    )
    if db_transactions:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already transaction code",
        )

    data = transaction.dict()
    db_transaction.update(**data)

    db_transaction.updated_date = datetime.datetime.now()
    db_transaction.save()
    db_transaction.reload()
    return db_transaction


@router.delete(
    "/{transaction_id}/delete",
    response_model_by_alias=False,
)
async def delete(
    transaction_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.transactions.Account:
    try:
        db_transaction = models.Account.objects.get(id=transaction_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this transaction",
        )
    db_transaction.update(status="disactive", updated_date=datetime.datetime.now())
    db_transaction.reload()
    db_transaction.save()

    divisions = models.Division.objects(transaction=db_transaction, status="active")
    for division in divisions:
        division.status = "disactive"
        division.save()
    return db_transaction
