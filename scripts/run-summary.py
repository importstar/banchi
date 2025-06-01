import sys

from banchi.api import models, schemas
import datetime
import asyncio
import decimal
import bson
import calendar


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

    # import pprint

    # print('decrease ->')
    # pprint.pprint(decrease_month_account_summary)
    # print('increase ->')
    # pprint.pprint(increase_month_account_summary)

    if not decrease_month_account_summary and not increase_month_account_summary:
        return 

    increase_min_year = min(
            increase_month_account_summary.keys(), default=0
        )
    decrease_min_year = min(
        decrease_month_account_summary.keys(), default=0
    )

    min_year = increase_min_year
    if decrease_min_year > 0 and decrease_min_year < min_year:
        min_year = decrease_min_year

    if not min_year:
        return 


    for year_iter in range(min_year, datetime.datetime.now().year + 1):
        for month_iter in range(1, 13):
            print('->', year_iter, month_iter)

            db_account_book_summary = await models.account_books.AccountBookSummary.find_one(
                models.AccountBookSummary.account_book.id==db_account_book.id,
                models.AccountBookSummary.year==year_iter,
                models.AccountBookSummary.month==month_iter,
            )


            decrease_month_result_check = all(
                [
                    year_iter  in decrease_month_account_summary,
                    month_iter  in decrease_month_account_summary.get(year_iter,[]),
                ])
            
            increase_month_result_check = all(
                [
                    year_iter  in increase_month_account_summary,
                    month_iter in increase_month_account_summary.get(year_iter,[]),
                ]
            )
            

            if not decrease_month_result_check and not increase_month_result_check:
                if db_account_book_summary:
                    await db_account_book_summary.delete()
                continue

            if not db_account_book_summary:
                db_account_book_summary = models.account_books.AccountBookSummary(
                    account_book=db_account_book,
                    year=year_iter,
                    month=month_iter,
                    date=datetime.datetime(year=year_iter, month=month_iter, day=calendar.monthrange(year_iter,month_iter)[1])
                )

            decrease = 0
            increase = 0
            balance = 0
            if decrease_month_result_check:
                decrease = decrease_month_account_summary[year_iter][month_iter]

            if increase_month_result_check:
                increase = increase_month_account_summary[year_iter][month_iter]


            if type(decrease) is bson.Decimal128:
                decrease = decrease.to_decimal()

            if type(increase) is bson.Decimal128:
                increase = increase.to_decimal()

            if db_account_book.type in ["income", "equity", "liability"]:
                balance = decrease - increase
            else:
                balance = increase - decrease

            db_account_book_summary.balance = balance
            db_account_book_summary.increase = increase
            db_account_book_summary.decrease = decrease

            await db_account_book_summary.save()



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
        await get_account_book_balance(account_book)
        print("check account book id:", account_book.name)


if __name__ == "__main__":
    asyncio.run(main())
