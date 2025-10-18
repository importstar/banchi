import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status, Query

from loguru import logger

import bson
import typing
import math
import decimal
import calendar

from beanie.operators import Inc, Set, In, Or, And, RegEx

import re
from beanie import PydanticObjectId

from banchi.api import models
from banchi.api.core import deps
from banchi.api import schemas

router = APIRouter(prefix="/transaction-templates", tags=["transaction-templates"])


@router.get("")
async def get_all() -> schemas.transactions.TransactionTemplateList:
    # print(">>>", page, size_per_page)
    return dict()


@router.post("")
async def create(
    transaction: schemas.transactions.CreatedTransactionTemplate,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplate:
    return ""


@router.get("/{transaction_id}")
async def get(
    transaction_id: PydanticObjectId,
    db_transaction: typing.Annotated[
        models.transactions.TransactionTemplate, Depends(deps.get_transaction)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplate:

    return db_transaction


@router.put("/{transaction_id}")
async def update(
    transaction_id: PydanticObjectId,
    transaction: schemas.transactions.UpdatedTransactionTemplate,
    db_transaction: typing.Annotated[
        models.transactions.TransactionTemplate, Depends(deps.get_transaction)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplate:

    return db_transaction


@router.delete(
    "/{transaction_id}",
)
async def delete(
    transaction_id: PydanticObjectId,
    db_transaction: typing.Annotated[
        models.transactions.TransactionTemplate, Depends(deps.get_transaction)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplate:
    db_transaction.status = "delete"
    db_transaction.updated_date = datetime.datetime.now()
    db_transaction.updated_by = current_user
    await db_transaction.save()


@router.get("/tags/{tag}")
async def get_by_tags(
    tag: str,
    db_transactions: typing.Annotated[
        models.transactions.TransactionTemplate, Depends(deps.get_transactions_by_tag)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplateList:

    return dict(transactions=db_transactions)
