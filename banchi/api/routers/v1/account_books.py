import datetime
import calendar
import io
import bson
import decimal
import typing

from fastapi import APIRouter, Depends, HTTPException, Response, status

from loguru import logger

from beanie import PydanticObjectId
from beanie.operators import Inc, Set, In

from banchi.api import models
from banchi.api.core import deps
from banchi.api import schemas

router = APIRouter(prefix="/account-books", tags=["account_books"])


@router.get("")
async def get_all(
    account_id: PydanticObjectId,
    db_account_books: typing.Annotated[
        list[models.account_books.AccountBook],
        Depends(deps.get_account_books_by_account),
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.account_books.AccountBookList:
    return dict(account_books=db_account_books)


@router.post("")
async def create(
    account_book: schemas.account_books.CreatedAccountBook,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBook:
    db_account = await deps.get_account(account_book.account_id, current_user)

    db_parent_account_book = None
    if account_book.parent_id:
        db_parent_account_book = await deps.get_account_book(
            account_book.parent_id, current_user
        )

    data = account_book.dict()
    data["creator"] = current_user
    data["updated_by"] = current_user
    data["account"] = db_account
    data["parent"] = db_parent_account_book

    db_account_book = models.account_books.AccountBook.parse_obj(data)
    await db_account_book.save()

    # await db_account_book.fetch_links()

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


@router.get("/{account_book_id}/children")
async def get_children(
    account_book_id: PydanticObjectId,
    db_account_book: typing.Annotated[
        models.account_books.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBookList:

    pipline = [
        {"$match": {"_id": db_account_book.id, "status": "active"}},
        {
            "$graphLookup": {
                "from": "account_books",
                "startWith": "$_id",
                "connectFromField": "_id",
                "connectToField": "parent.$id",
                "as": "children",
                "maxDepth": 0,
                "restrictSearchWithMatch": {"status": "active"},
            }
        },
    ]

    account_book_agg = (
        await models.account_books.AccountBook.find().aggregate(pipline).to_list()
    )

    children_ids = []
    if len(account_book_agg) > 0:
        children_ids = [c["_id"] for c in account_book_agg[0]["children"]]

    db_account_books = await models.account_books.AccountBook.find(
        In(models.account_books.AccountBook.id, children_ids), fetch_links=True
    ).to_list()

    return dict(account_books=db_account_books)


async def get_account_book_balance_by_trasaction(
    db_account_book, attribute="from_account_book"
):
    account_book_agg = (
        await models.transactions.Transaction.find()
        .aggregate(
            [
                {
                    "$match": {
                        f"{attribute}.$id": db_account_book.id,
                        "status": "active",
                    }
                },
                {
                    "$group": {
                        "_id": f"${attribute}._id",
                        "total": {"$sum": "$value"},
                    }
                },
            ],
        )
        .to_list()
    )

    value = account_book_agg[0]["total"].to_decimal() if account_book_agg else 0

    return value


async def get_account_book_balance_by_account_book_summary(db_account_book):

    pipline = [
        {"$match": {"_id": db_account_book.id, "status": "active"}},
        {
            "$graphLookup": {
                "from": "account_books",
                "startWith": "$_id",
                "connectFromField": "_id",
                "connectToField": "parent.$id",
                "as": "children",
            }
        },
        {"$unwind": {"path": "$children"}},
        {
            "$group": {
                "_id": None,
                "quantity": {"$sum": 1},
                "balance": {"$sum": "$children.balance"},
                # "increase": {"$sum": "$children.increase"},
                # "decrease": {"$sum": "$children.decrease"},
            }
        },
    ]

    account_book_agg = (
        await models.account_books.AccountBook.find().aggregate(pipline).to_list()
    )

    data = dict()
    if len(account_book_agg) > 0:
        data = account_book_agg[0]

    results = dict(
        balance=decimal.Decimal(0),
        # increase=decimal.Decimal(0),
        # decrease=decimal.Decimal(0),
        quantity=0,
    )
    if "_id" in data:
        data.pop("_id")

    for key in results.keys():
        if key == "quantity":
            results[key] = data.get(key, 0) + getattr(db_account_book, key, 0)
        else:
            results[key] = decimal.Decimal(str(data.get(key, 0))) + decimal.Decimal(
                str(getattr(db_account_book, key, 0))
            )

    results["quantity"] += 1

    return results


async def get_account_book_balance_by_trasaction(
    db_account_book, receive=False
) -> schemas.account_books.AccountBookBalance:
    balance = increase = decrease = 0

    decrease = await get_account_book_balance_by_trasaction(
        db_account_book, "from_account_book"
    )
    increase = await get_account_book_balance_by_trasaction(
        db_account_book, "to_account_book"
    )

    if db_account_book.type in ["income", "equity", "liability", "credit_card"]:
        balance = decrease - increase
    else:
        balance = increase - decrease

    account_book_balance = schemas.account_books.AccountBookBalance(
        id=db_account_book.id,
        type=db_account_book.type,
        balance=balance,
        decrease=decrease,
        increase=increase,
        net_balance=balance,
        net_decrease=decrease,
        net_increase=increase,
    )

    if not receive:
        return account_book_balance

    account_book_children = await models.account_books.AccountBook.find(
        models.account_books.AccountBook.parent.id == db_account_book.id,
        models.account_books.AccountBook.status == "active",
    ).to_list()

    for account_book_child in account_book_children:
        child_account_book_balance = await get_account_book_balance_by_trasaction(
            account_book_child,
            True,
        )
        account_book_balance.net_balance += child_account_book_balance.net_balance
        account_book_balance.net_increase += child_account_book_balance.net_increase
        account_book_balance.net_decrease += child_account_book_balance.net_decrease
        account_book_balance.children.append(child_account_book_balance)

    return account_book_balance


async def get_account_book_balance_by_summary(
    db_account_book, receive=False
) -> schemas.account_books.AccountBookBalance:
    balance = increase = decrease = 0

    results = await get_account_book_balance_by_account_book_summary(db_account_book)

    net_balance = results.get("balance", 0)

    account_book_balance = schemas.account_books.AccountBookBalance(
        id=db_account_book.id,
        balance=db_account_book.balance,
        net_balance=net_balance,
        children=results.get("quantity", 0),
    )

    # print(account_book_balance)
    return account_book_balance


@router.get(
    "/{account_book_id}/balance",
)
async def get_balance(
    account_book_id: PydanticObjectId,
    db_account_book: typing.Annotated[
        models.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBookBalance:

    return await get_account_book_balance_by_summary(db_account_book)


@router.get(
    "/{account_book_id}/summary/{year}/{month}",
)
async def get_summary_by_year_month(
    account_book_id: PydanticObjectId,
    year: int,
    month: int,
    db_account_book: typing.Annotated[
        models.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBookSummary:
    db_account_book_summary = await models.account_books.AccountBookSummary.find_one(
        models.account_books.AccountBookSummary.account_book.id == db_account_book.id,
        models.account_books.AccountBookSummary.year == year,
        models.account_books.AccountBookSummary.month == month,
    )

    if not db_account_book_summary:
        db_account_book_summary = models.account_books.AccountBookSummary(
            account_book=db_account_book,
            year=year,
            month=month,
            date=datetime.datetime.now(),
        )

    return db_account_book_summary


@router.get(
    "/{account_book_id}/balance/{year}/{month}",
)
async def get_balance_by_year_month(
    account_book_id: PydanticObjectId,
    year: int,
    month: int,
    db_account_book: typing.Annotated[
        models.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> dict:

    first_day_of_next_month = datetime.datetime(
        year, month, calendar.monthrange(year, month)[1]
    ) + datetime.timedelta(days=1)
    db_account_book_balance = (
        await models.account_books.AccountBookSummary.find(
            models.account_books.AccountBookSummary.account_book.id
            == db_account_book.id,
            models.account_books.AccountBookSummary.date < first_day_of_next_month,
        )
        .aggregate(
            [
                {
                    "$group": {
                        "_id": None,
                        # "increase": {"$sum": "$increase"},
                        # "decrease": {"$sum": "$decrease"},
                        "balance": {"$sum": "$balance"},
                    }
                }
            ]
        )
        .to_list()
    )

    result = dict(balance=decimal.Decimal("0"))
    if len(db_account_book_balance) > 0:
        result = dict(
            balance=db_account_book_balance[0]
            .get("balance", bson.Decimal128("0"))
            .to_decimal()
        )
    return result


@router.get(
    "/{account_book_id}/summaries",
)
async def get_summaries(
    account_book_id: PydanticObjectId,
    db_account_book: typing.Annotated[
        models.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBookSummaryList:

    db_account_book_summary = await models.account_books.AccountBookSummary.find(
        models.account_books.AccountBookSummary.account_book.id == db_account_book.id,
    ).to_list()

    return schemas.account_books.AccountBookSummaryList(
        account_book_summaries=db_account_book_summary
    )


@router.put("/{account_book_id}")
async def update(
    account_book_id: str,
    account_book: schemas.account_books.UpdatedAccountBook,
    db_account_book: typing.Annotated[
        models.account_books.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBook:
    data = account_book.dict()
    await db_account_book.update(Set(data))

    db_account_book.parent = await models.account_books.AccountBook.get(
        account_book.parent_id
    )
    db_account_book.updated_by = current_user
    db_account_book.updated_date = datetime.datetime.now()
    await db_account_book.save()

    return db_account_book


@router.delete("/{account_book_id}")
async def delete(
    db_account_book: typing.Annotated[
        models.account_books.AccountBook, Depends(deps.get_account_book)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.account_books.AccountBook:
    db_account_book.status = "delete"
    db_account_book.updated_date = datetime.datetime.now()
    db_account_book.updated_by = current_user
    await db_account_book.save()
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
        liability=dict(positive="increase", negative="decrease"),
        credit_card=dict(positive="payment", negative="charge"),
    )
    type_name = db_account_book.type
    if type_name == "credit card":
        type_name = "credit_card"
    return labels[type_name]
