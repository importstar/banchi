import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status

from loguru import logger

from banchiapi import models
from banchiapi.core import deps
from banchiapi import schemas

router = APIRouter(prefix="/account_book-books", tags=["account_book book"])


@router.get(
    "",
    response_model_by_alias=False,
)
async def get_account_books(
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBookList:
    account_books = await models.account_books.AccountBook.find(
        owner=current_user
    ).to_list()
    return account_books


@router.post(
    "/create",
    response_model_by_alias=False,
)
async def create_account_book(
    account_book: schemas.account_books.CreatedAccountBook,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBook:
    db_account_book = models.AccountBook.objects(
        name=account_book.name, status="active"
    ).first()
    if db_account_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already account_book name",
        )
    db_account_book = models.AccountBook.objects(
        code=account_book.code, status="active"
    ).first()
    if db_account_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already account_book code",
        )

    data = account_book.dict()
    db_account_book = models.AccountBook(**data)
    db_account_book.created_date = datetime.datetime.now()
    db_account_book.updated_date = datetime.datetime.now()
    db_account_book.save()

    return db_account_book


@router.get(
    "/{account_book_id}",
    response_model_by_alias=False,
    response_model=schemas.account_books.AccountBook,
)
def get_account_book(
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
    return db_account_book


@router.put(
    "/{account_book_id}/update",
    response_model_by_alias=False,
    response_model=schemas.account_books.AccountBook,
)
def update_account_book(
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
def delete_account_book(
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
