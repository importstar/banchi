import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status

from loguru import logger

import bson
import typing
from beanie.odm.operators.find.logical import Or, And
from beanie.operators import Inc, Set

from beanie import PydanticObjectId

from banchiapi import models
from banchiapi.core import deps
from banchiapi import schemas

router = APIRouter(prefix="/transactions", tags=["transactions"])


async def transform_transaction(transaction, current_user):
    db_from_account_book = await deps.get_account_book(
        transaction.from_account_book_id, current_user
    )
    db_to_account_book = await deps.get_account_book(
        transaction.to_account_book_id, current_user
    )

    if not (db_from_account_book and db_to_account_book):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AccountBook id {transaction.account_book_id} not found",
        )

    data = transaction.dict()
    data["from_account_book"] = db_from_account_book
    data["to_account_book"] = db_to_account_book

    if transaction.value < 0:
        data["from_account_book"] = db_to_account_book
        data["to_account_book"] = db_from_account_book
        data["value"] *= -1

    data["updated_date"] = datetime.datetime.now()
    data["updated_by"] = current_user

    return data


@router.get("")
async def get_all(
    from_account_book_id: PydanticObjectId | None,
    to_account_book_id: PydanticObjectId | None,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionList:
    query_args = [
        models.transactions.Transaction.status == "active",
    ]

    from_account_books = []
    to_account_books = []
    all_transactions = []
    if from_account_book_id:
        from_account_book = await deps.get_account_book(
            from_account_book_id, current_user
        )
        if from_account_book:
            from_account_books = await models.transactions.Transaction.find(
                *query_args,
                models.transactions.Transaction.from_account_book.id
                == from_account_book_id,
                fetch_links=True,
            ).to_list()

    if to_account_book_id:
        to_account_book = await deps.get_account_book(to_account_book_id, current_user)
        if to_account_book:
            to_account_books = await models.transactions.Transaction.find(
                *query_args,
                models.transactions.Transaction.to_account_book.id
                == to_account_book_id,
                fetch_links=True,
            ).to_list()

    if not from_account_book_id and not to_account_book_id:
        all_transactions = await query.to_list()

    db_transactions = all_transactions + to_account_books + from_account_books
    db_transactions.sort(key=lambda t: t.date, reverse=True)

    return dict(transactions=db_transactions)


@router.post("")
async def create(
    transaction: schemas.transactions.CreatedTransaction,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.Transaction:
    data = await transform_transaction(transaction, current_user)
    data["creator"] = current_user

    db_transaction = models.transactions.Transaction.parse_obj(data)
    await db_transaction.save()

    return db_transaction


@router.get("/{transaction_id}")
async def get(
    transaction_id: PydanticObjectId,
    db_transaction: typing.Annotated[
        models.transactions.Transaction, Depends(deps.get_transaction)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.Transaction:
    return db_transaction


@router.put("/{transaction_id}")
async def update(
    transaction_id: PydanticObjectId,
    transaction: schemas.transactions.UpdatedTransaction,
    db_transaction: typing.Annotated[
        models.transactions.Transaction, Depends(deps.get_transaction)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.Transaction:
    data = transaction.dict()
    await db_transaction.update(Set(data))

    data = await transform_transaction(transaction, current_user)
    db_transaction.value = data["value"]
    db_transaction.to_account_book = data["to_account_book"]
    db_transaction.from_account_book = data["from_account_book"]
    await db_transaction.save()

    await db_transaction.fetch_all_links()
    return db_transaction


@router.delete(
    "/{transaction_id}",
)
async def delete(
    transaction_id: PydanticObjectId,
    db_transaction: typing.Annotated[
        models.transactions.Transaction, Depends(deps.get_transaction)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.Transaction:
    db_transaction.status = "delete"
    db_transaction.updated_date = datetime.datetime.now()
    db_transaction.updated_by = current_user
    await db_transaction.save()

    return db_transaction
