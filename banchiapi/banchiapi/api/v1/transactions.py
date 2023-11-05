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
    from_account_book_id: str | None,
    to_account_book_id: str | None,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.transactions.TransactionList:
    query = models.transactions.Transaction.find(
        models.transactions.Transaction.status == "active",
        models.transactions.Transaction.creator.id == current_user.id,
        fetch_links=True,
    )

    if from_account_book_id:
        query.update(
            models.transactions.Transaction.from_account_book.id
            == bson.ObjectId(from_account_book_id)
        )
    if to_account_book_id:
        query.update(
            models.transactions.Transaction.to_account_book.id
            == bson.ObjectId(to_account_book_id)
        )

    db_transactions = await query.to_list()

    return dict(transactions=db_transactions)


@router.post(
    "/create",
    response_model_by_alias=False,
)
async def create(
    transaction: schemas.transactions.CreatedTransaction,
    current_user: Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.transactions.Transaction:
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
    data["creator"] = current_user
    data["updated_by"] = current_user
    data["from_account_book"] = db_from_account_book
    data["to_account_book"] = db_to_account_book

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
    transaction: schemas.transactions.CreatedTransaction,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.transactions.Transaction:
    db_transaction = models.Transaction.objects(id=transaction_id).first()
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    db_transactions = models.Transaction.objects(
        name=transaction.name, status="active", id__ne=transaction_id
    )
    if db_transactions:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already transaction name",
        )
    db_transactions = models.Transaction.objects(
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
