import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status

from loguru import logger

import bson
from typing import Annotated
from beanie.odm.operators.find.logical import Or, And

from banchiapi import models
from banchiapi.core import deps
from banchiapi import schemas

router = APIRouter(prefix="/transactions", tags=["transactions"])


def transform_transaction(tranasction):
    db_from_account_book = await models.account_books.AccountBook.find_one(
        models.account_books.AccountBook.id
        == bson.ObjectId(transaction.from_account_book_id),
        models.account_books.AccountBook.creator.id == current_user.id,
    )
    db_to_account_book = await models.account_books.AccountBook.find_one(
        models.account_books.AccountBook.id
        == bson.ObjectId(transaction.to_account_book_id),
        models.account_books.AccountBook.creator.id == current_user.id,
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

    data["amount"] = data["value"] * db_from_account_book.smallest_fraction

    data["updated_date"] = datetime.datetime.now()

    return data


@router.get(
    "",
    response_model_by_alias=False,
)
async def get_all(
    from_account_book_id: str | None,
    to_account_book_id: str | None,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.transactions.TransactionList:
    query_args = [
        models.transactions.Transaction.status == "active",
        models.transactions.Transaction.creator.id == current_user.id,
    ]

    from_account_books = []
    to_account_books = []
    all_transactions = []
    if from_account_book_id:
        from_account_books = await models.transactions.Transaction.find(
            *query_args,
            models.transactions.Transaction.from_account_book.id
            == bson.ObjectId(from_account_book_id),
            fetch_links=True,
        ).to_list()

    if to_account_book_id:
        to_account_books = await models.transactions.Transaction.find(
            *query_args,
            models.transactions.Transaction.to_account_book.id
            == bson.ObjectId(to_account_book_id),
            fetch_links=True,
        ).to_list()

    if not from_account_book_id and not to_account_book_id:
        all_transactions = await query.to_list()

    db_transactions = all_transactions + to_account_books + from_account_books
    db_transactions.sort(key=lambda t: t.date)

    return dict(transactions=db_transactions)


@router.post(
    "/create",
    response_model_by_alias=False,
)
async def create(
    transaction: schemas.transactions.CreatedTransaction,
    current_user: Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.Transaction:
    data = transform_transaction(transaction)
    data["creator"] = current_user
    data["updated_by"] = current_user

    db_transaction = models.transactions.Transaction.parse_obj(data)
    await db_transaction.save()

    return db_transaction


@router.get(
    "/{transaction_id}",
    response_model_by_alias=False,
)
async def get(
    transaction_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.transactions.Transaction:
    db_transaction = await models.transactions.Transaction.find_one(
        models.transactions.Transaction.id == bson.ObjectId(transaction_id),
        models.transactions.Transaction.creator.id == current_user.id,
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
    transaction: schemas.transactions.UpdatedTransaction,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.transactions.Transaction:
    db_transaction = await models.transactions.Transaction.get(transaction_id)
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )

    data = transform_transaction(transaction)

    data["updated_by"] = current_user
    await db_transaction.set(data)

    await db_transaction.fetch_all_links()
    return db_transaction


@router.delete(
    "/{transaction_id}/delete",
    response_model_by_alias=False,
)
async def delete(
    transaction_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.transactions.Transaction:
    try:
        db_transaction = models.Transaction.objects.get(id=transaction_id)
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
