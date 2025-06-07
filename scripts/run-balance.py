import sys

from banchi.api import models, schemas
import datetime
import asyncio


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


async def get_account_book_balance(
    db_account_book, receive=False
) -> schemas.account_books.AccountBookBalance:
    balance = increase = decrease = 0

    decrease = await get_account_book_balance_by_trasaction(
        db_account_book, "from_account_book"
    )
    increase = await get_account_book_balance_by_trasaction(
        db_account_book, "to_account_book"
    )

    if db_account_book.type in ["income", "equity"]:
        balance = decrease - increase
    else:
        balance = increase - decrease

    # db_account_book.increase = increase
    # db_account_book.decrease = decrease
    db_account_book.balance = balance
    await db_account_book.save()
    return balance


async def create_user_admin():
    class Setting:
        def __init__(self):
            self.MONGODB_URI = "mongodb://localhost/banchidb"

    settings = Setting()
    if len(sys.argv) > 1:
        settings.MONGODB_URI = sys.argv[1]

    await models.init_beanie(None, settings)

    print("balance checker")
    account_books = await models.account_books.AccountBook.find(
        models.account_books.AccountBook.status == "active"
    ).to_list()
    for account_book in account_books:
        balance = await get_account_book_balance(account_book)
        print(f"check {account_book.name:<50} balance:{str(balance)}")


if __name__ == "__main__":
    asyncio.run(create_user_admin())
