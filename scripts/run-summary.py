import sys

from banchi.api import models, schemas
import datetime
import asyncio


async def get_account_book_balance_by_trasaction(
    db_account_book, attribute="from_account_book"
):
    account_book_agg = await models.transactions.Transaction.aggregate(
        [
            {
                "$match": {
                    f"{attribute}.$id": db_account_book.id,
                    "status": "active",
                }
            },
            {
                "$group": {
                    "_id": {
                        "account_book_id": db_account_book.id,
                        "month": {"$month": "$date"},
                        "year": {"$year": "$date"},
                    },
                    "total": {"$sum": "$value"},
                }
            },
            {
                "$sort": {
                    "_id.year": 1,
                    "_id.month": 1,
                }
            },
            {
                "$addFields": {
                    "year": "$_id.year",
                    "month": "$_id.month",
                    "account_book_id": "$_id.account_book_id",
                }
            },
            {
                "$project": {
                    "account_book_id": 1,
                    "year": 1,
                    "month": 1,
                    "total": 1,
                }
            },
        ],
    ).to_list()

    datas = {}

    for data in account_book_agg:
        year = data["year"]
        month = data["month"]
        if year not in datas:
            datas[year] = {}
        if month not in datas[year]:
            datas[year][month] = 0
        datas[year][month] = data["total"]

    return datas


async def get_account_book_balance(
    db_account_book, receive=False
) -> schemas.account_books.AccountBookBalance:
    balance = increase = decrease = 0

    decrease_month_account_summary = await get_account_book_balance_by_trasaction(
        db_account_book, "from_account_book"
    )

    increase_month_account_summary = await get_account_book_balance_by_trasaction(
        db_account_book, "to_account_book"
    )

    import pprint

    pprint.pprint(decrease_month_account_summary)
    pprint.pprint(increase_month_account_summary)

    return 0
    min_year = 0
    min_month = 0
    if decrease_month_account_summary or increase_month_account_summary:
        doc_min_year = min(
            increase_month_account_summary[:1] + decrease_month_account_summary[:1],
            key=lambda x: x["year"],
        )

        doc_min_month = min(
            increase_month_account_summary[:1] + decrease_month_account_summary[:1],
            key=lambda x: x["month"],
        )

        min_year = doc_min_year["year"]
        min_month = doc_min_month["month"]

    print(min_year, min_month)
    return 0
    for year_iter in range(min_year, datetime.datetime.now().year + 1):
        for month_iter in range(1, 13):

            decrease_month = next(
                (
                    item
                    for item in decrease_month_account_summary
                    if item["_id"]["year"] == year_iter
                    and item["_id"]["month"] == month_iter
                ),
                None,
            )
            increase_month = next(
                (
                    item
                    for item in increase_month_account_summary
                    if item["_id"]["year"] == year_iter
                    and item["_id"]["month"] == month_iter
                ),
                None,
            )
            print(f"{increase_month_account_summary}")

            print(f"checking: \n{decrease_month=}, \n{increase_month=}")

            decrease = increase = 0
            if decrease_month:
                decrease = decrease_month["total"] if decrease_month else 0
            if increase_month:
                increase = increase_month["total"] if increase_month else 0

    if db_account_book.type in ["income", "equity", "liability"]:
        balance = decrease - increase
    else:
        balance = increase - decrease

    # db_account_book.increase = increase
    # db_account_book.decrease = decrease
    db_account_book.balance = balance
    await db_account_book.save()
    return balance


async def main():
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
        print("check account book id:", account_book.name, balance)


if __name__ == "__main__":
    asyncio.run(main())
