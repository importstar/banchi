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
async def get_all(
    account_id: PydanticObjectId | None,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
    page: typing.Annotated[int | None, Query()] = 1,
    size_per_page: typing.Annotated[int | None, Query()] = 50,
) -> schemas.transactions.TransactionTemplateList:
    # print(">>>", page, size_per_page)
    return dict()


@router.post("")
async def create(
    transaction: schemas.transactions.CreatedTransactionTemplate,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplate:
    return ""


@router.get("/{transaction_template_id}")
async def get(
    transaction_template_id: PydanticObjectId,
    db_transaction_template: typing.Annotated[
        models.transactions.TransactionTemplate, Depends(deps.get_transaction_template)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplate:

    return db_transaction_template


@router.put("/{transaction_template_id}")
async def update(
    transaction_template_id: PydanticObjectId,
    transaction_template: schemas.transactions.UpdatedTransactionTemplate,
    db_transaction_template: typing.Annotated[
        models.transactions.TransactionTemplate, Depends(deps.get_transaction_template)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplate:

    return db_transaction_template




@router.delete(
    "/{transaction_template_id}",
)
async def delete(
    transaction_template_id: PydanticObjectId,
    db_transaction_template: typing.Annotated[
        models.transactions.TransactionTemplate, Depends(deps.get_transaction_template)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplate:
    db_transaction_template.status = "delete"
    db_transaction_template.updated_date = datetime.datetime.now()
    db_transaction_template.updated_by = current_user
    await db_transaction_template.save()


@router.get("/tags/{tag}")
async def get_by_tags(
    tag: str,
    db_transactions: typing.Annotated[
        models.transactions.TransactionTemplate, Depends(deps.get_transactions_by_tag)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplateList:

    return dict(transactions=db_transactions)
