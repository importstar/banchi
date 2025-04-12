import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status, Query

from loguru import logger

import bson
import typing
import math
from beanie.odm.operators.find.logical import Or, And
from beanie.operators import Inc, Set

from beanie import PydanticObjectId

from banchi.api import models
from banchi.api.core import deps
from banchi.api import schemas

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
    page: typing.Annotated[int | None, Query()] = 1,
    size_per_page: typing.Annotated[int | None, Query()] = 50,
) -> schemas.transactions.TransactionList:
    # print(">>>", page, size_per_page)
    from_account_book = None
    to_account_book = None

    account_book_query = []
    if from_account_book_id:
        from_account_book = await deps.get_account_book(
            from_account_book_id, current_user
        )
        account_book_query = (
            models.transactions.Transaction.from_account_book.id == from_account_book_id
        )
    if to_account_book_id:
        to_account_book = await deps.get_account_book(to_account_book_id, current_user)
        account_book_query = (
            models.transactions.Transaction.to_account_book.id == to_account_book_id
        )

    if from_account_book_id and to_account_book_id:
        account_book_query = Or(
            models.transactions.Transaction.from_account_book.id
            == from_account_book_id,
            models.transactions.Transaction.to_account_book.id == to_account_book_id,
        )

    query_args = [
        models.transactions.Transaction.status == "active",
        account_book_query,
    ]

    transaction_count = await models.transactions.Transaction.find(
        *query_args,
    ).count()

    db_transactions = (
        await models.transactions.Transaction.find(
            *query_args, fetch_links=True, nesting_depth=1
        )
        .sort(-models.transactions.Transaction.date)
        .limit(size_per_page)
        .skip((page - 1) * size_per_page)
        .to_list()
    )

    return dict(
        transactions=db_transactions,
        page=page,
        size_per_page=size_per_page,
        page_size=int(math.ceil(transaction_count / size_per_page)),
    )


@router.get("/get_recursive")
async def get_recursive(
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

    db_from_account_book = data["from_account_book"]
    db_to_account_book = data["to_account_book"]

    if db_from_account_book.type in ["income", "equity", "liability"]:
        db_from_account_book.balance += data["value"]
    else:
        db_from_account_book.balance -= data["value"]

    if db_to_account_book.type in ["income", "equity", "liability"]:
        db_to_account_book.balance -= data["value"]
    else:
        db_to_account_book.balance += data["value"]

    db_from_account_book.decrease += data["value"]
    db_to_account_book.increase += data["value"]

    await db_to_account_book.save()
    await db_from_account_book.save()

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

    if db_transaction.from_account_book != data["from_account_book_id"]:
        db_transaction.from_account_book.balance -= db_transaction.value
        db_transaction.from_account_book.decrease += db_transaction.value
    else:
        db_transaction.from_account_book.balance += db_transaction.value
        db_transaction.from_account_book.increase -= db_transaction.value
    if db_transaction.to_account_book != data["to_account_book_id"]:
        db_transaction.to_account_book.balance += db_transaction.value
        db_transaction.to_account_book.increase -= db_transaction.value
    else:
        db_transaction.to_account_book.balance -= db_transaction.value
        db_transaction.to_account_book.decrease += db_transaction.value
    await db_transaction.to_account_book.save()
    await db_transaction.from_account_book.save()

    db_transaction.to_account_book = data["to_account_book"]
    db_transaction.from_account_book = data["from_account_book"]
    db_transaction.updated_date = datetime.datetime.now()
    db_transaction.updated_by = current_user

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

    to_account_book = db_transaction.to_account_book
    from_account_book = db_transaction.from_account_book

    to_account_book.balance -= db_transaction.value
    from_account_book.balance += db_transaction.value

    to_account_book.increase -= db_transaction.value
    from_account_book.decrease += db_transaction.value

    to_account_book.save()
    from_account_book.save()

    await db_transaction.save()

    return db_transaction


@router.get("/tags/{tag}")
async def get_by_tags(
    tag: str,
    db_transactions: typing.Annotated[
        models.transactions.Transaction, Depends(deps.get_transactions_by_tag)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.TransactionList:

    return dict(transactions=db_transactions)
