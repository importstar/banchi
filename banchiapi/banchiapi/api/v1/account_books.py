import datetime
import io
import bson

from fastapi import APIRouter, Depends, HTTPException, Response, status

from loguru import logger

from banchiapi import models
from banchiapi.core import deps
from banchiapi import schemas

router = APIRouter(prefix="/account-books", tags=["account_books"])


@router.get(
    "",
    response_model_by_alias=False,
)
async def get_all(
    current_user: models.users.User = Depends(deps.get_current_user),
    account_id: str | None = None,
) -> schemas.account_books.AccountBookList:
    query = models.account_books.AccountBook.find(
        models.account_books.AccountBook.status == "active",
        models.account_books.AccountBook.creator.id == current_user.id,
    )
    if account_id:
        query.find(
            models.account_books.AccountBook.account.id == bson.ObjectId(account_id)
        )

    account_books = await query.find(fetch_links=True).to_list()
    return dict(account_books=account_books)


@router.post(
    "/create",
    response_model_by_alias=False,
)
async def create(
    account_book: schemas.account_books.CreatedAccountBook,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBook:
    data = account_book.dict()

    db_account = await models.accounts.Account.find_one(
        models.accounts.Account.id == bson.ObjectId(data["account_id"]),
        models.accounts.Account.status == "active",
        models.accounts.Account.creator.id == current_user.id,
    )

    db_parent_account_book = None
    if data.get("parent_id"):
        db_parent_account_book = await models.account_books.AccountBook.find_one(
            models.account_books.AccountBook.id == bson.ObjectId(data["parent_id"]),
            models.account_books.AccountBook.status == "active",
            models.account_books.AccountBook.creator.id == current_user.id,
        )

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


@router.get(
    "/{account_book_id}",
    response_model_by_alias=False,
)
async def get(
    account_book_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBook:
    db_account_book = await models.account_books.AccountBook.find_one(
        models.account_books.AccountBook.id == bson.ObjectId(account_book_id),
        models.account_books.AccountBook.creator.id == current_user.id,
        models.account_books.AccountBook.status == "active",
        fetch_links=True,
    )
    if not db_account_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this account_book",
        )
    return db_account_book


@router.put(
    "/{account_book_id}/update",
    response_model_by_alias=False,
    response_model=schemas.account_books.AccountBook,
)
async def update(
    account_book_id: str,
    account_book: schemas.account_books.CreatedAccountBook,
    current_user: models.users.User = Depends(deps.get_current_user),
):
    db_account_book = models.AccountBook.objects(id=account_book_id).first()
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


@router.delete(
    "/{account_book_id}/delete",
    response_model_by_alias=False,
    response_model=schemas.account_books.AccountBook,
)
async def delete(
    account_book_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
):
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
