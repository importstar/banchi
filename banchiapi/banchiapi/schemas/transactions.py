from bson import ObjectId

from pydantic import BaseModel, Field
from beanie import PydanticObjectId

from . import account_books
from . import accounts
from . import spaces
from . import bases


class BaseTransaction(BaseModel):
    desctiption: str = Field(..., example="Desctription")
    value: str = Field(..., example="0")
    currency: accounts.CurrencyEnum = Field(..., example=accounts.CurrencyEnum.THB)


class Transaction(bases.BaseSchema, BaseTransaction):
    from_account_book: account_books.ReferenceAccountBook
    to_account_book: account_books.ReferenceAccountBook
    status: str = Field(
        default="active",
        example="active",
    )


class TransactionList(BaseModel):
    transactions: list[Transaction]


class CreatedTransaction(BaseTransaction):
    from_account_id: str = Field(..., example="0")
    to_account_id: str = Field(..., example="0")
