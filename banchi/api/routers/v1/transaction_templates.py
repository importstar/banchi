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
    db_transaction_templates: typing.Annotated[
        list[models.transactions.TransactionTemplate],
        Depends(deps.get_transaction_templates),
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
    page: typing.Annotated[int | None, Query()] = 1,
    size_per_page: typing.Annotated[int | None, Query()] = 50,
) -> schemas.transactions.TransactionTemplateList:
    # print(">>>", page, size_per_page)
    transaction_templates = schemas.transactions.TransactionTemplateList(
        transaction_templates=db_transaction_templates,
        page=page,
        size_per_page=size_per_page,
    )

    return transaction_templates


@router.post("")
async def create(
    transaction_template: schemas.transactions.CreatedTransactionTemplate,
    account_id: PydanticObjectId,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplate:

    data = transaction_template.model_dump()

    data["creator"] = current_user
    data["updated_by"] = current_user
    data["account"] = await deps.get_account(account_id, current_user)

    db_transaction_template = models.transactions.TransactionTemplate.model_validate(
        data, strict=False
    )

    await db_transaction_template.save()

    return db_transaction_template


@router.get("/{transaction_template_id}")
async def get(
    transaction_template_id: PydanticObjectId,
    db_transaction_template: typing.Annotated[
        models.transactions.TransactionTemplate, Depends(deps.get_transaction_template)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionTemplate:
    print("xxx", db_transaction_template)

    return db_transaction_template


@router.put("/{transaction_template_id}")
async def update(
    transaction_template_id: PydanticObjectId,
    account_id: PydanticObjectId,
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
