import datetime
import io
import bson
import decimal
import typing

from fastapi import APIRouter, Depends, HTTPException, Response, status

from loguru import logger

from beanie import PydanticObjectId

from banchiapi import models
from banchiapi.core import deps
from banchiapi import schemas

router = APIRouter(prefix="/account-books", tags=["account_books"])


@router.get("")
async def get_all(
    account_id: PydanticObjectId,
    account_books: typing.Annotated[
        list[models.account_books.AccountBook],
        Depends(deps.get_account_books_by_account),
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.account_books.AccountBookList:
    return dict(account_books=account_books)


@router.post("")
async def create(
    account_book: schemas.account_books.CreatedAccountBook,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBook:
    data = account_book.dict()

    db_account = await deps.get_account(account_book.account_id, user)

    db_parent_account_book = None
    if data.get("parent_id"):
        db_parent_account_book = await deps.get_account(account_book.parent_id, user)

    data["creator"] = current_user
    data["updated_by"] = current_user
    data["account"] = db_account
    data["parent"] = db_parent_account_book

    db_account_book = models.account_books.AccountBook.parse_obj(data)
    await db_account_book.save()

    db_account_book = await models.account_books.AccountBook.get(
        db_account_book.id, fetch_links=True
    )

    return db_account_book


@router.get("/{account_book_id}")
async def get(
    account_book_id: PydanticObjectId,
    db_account_book: typing.Annotated[
        models.account_books.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBook:
    return db_account_book


@router.get(
    "/{account_book_id}/balance",
    response_model_by_alias=False,
)
async def get_balance(
    account_book_id: PydanticObjectId,
    db_account_book: typing.Annotated[
        models.account_books.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBookBalance:
    from_account_book_values = models.transactions.Transaction.find(
        models.transactions.Transaction.from_account_book.id == account_book_id
    )

    to_account_book_values = models.transactions.Transaction.find(
        models.transactions.Transaction.to_account_book.id == account_book_id
    )

    from_values = await from_account_book_values.sum(
        models.transactions.Transaction.value
    ) or decimal.Decimal(0)
    to_values = await to_account_book_values.sum(
        models.transactions.Transaction.value
    ) or decimal.Decimal(0)

    if from_values:
        from_values = from_values.to_decimal()
    if to_values:
        to_values = to_values.to_decimal()

    return dict(balance=to_values - from_values, decrese=from_values, increse=to_values)


@router.put("/{account_book_id}")
async def update(
    account_book_id: str,
    account_book: schemas.account_books.CreatedAccountBook,
    db_account_book: typing.Annotated[
        models.account_books.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBook:
    if not db_account_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    db_account_books = models.AccountBook.objects(
        name=account_book.name, status="active", id__ne=account_book_id
    )
    if db_account_books:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already account_book name",
        )
    db_account_books = models.AccountBook.objects(
        code=account_book.code, status="active", id__ne=account_book_id
    )
    if db_account_books:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already account_book code",
        )

    data = account_book.dict()
    db_account_book.update(**data)

    db_account_book.updated_date = datetime.datetime.now()
    db_account_book.save()
    db_account_book.reload()
    return db_account_book


@router.delete("/{account_book_id}/delete")
async def delete(
    account_book_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBook:
    try:
        db_account_book = models.AccountBook.objects.get(id=account_book_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this account_book",
        )
    db_account_book.update(status="disactive", updated_date=datetime.datetime.now())
    db_account_book.reload()
    db_account_book.save()

    divisions = models.Division.objects(account_book=db_account_book, status="active")
    for division in divisions:
        division.status = "disactive"
        division.save()
    return db_account_book


@router.get(
    "/{account_book_id}/label",
)
async def get_label(
    account_book_id: str,
    db_account_book: typing.Annotated[
        models.account_books.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBookLabel:
    labels = dict(
        asset=dict(positive="increase", negative="decrease"),
        cash=dict(positive="receive", negative="spend"),
        bank=dict(positive="deposit", negative="withdrawal"),
        equity=dict(positive="decrease", negative="increase"),
        expense=dict(positive="expense", negative="rebate"),
        income=dict(positive="charge", negative="income"),
        liability=dict(positive="decrease", negative="increase"),
        credit_card=dict(positive="payment", negative="charge"),
    )
    return labels[db_account_book.type]
