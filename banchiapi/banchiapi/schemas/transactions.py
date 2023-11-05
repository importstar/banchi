from bson import ObjectId

from pydantic import BaseModel, Field
from beanie import PydanticObjectId

from . import account_books
from . import accounts
from . import spaces
from . import users
from . import bases


class BaseTransaction(BaseModel):
    description: str = Field(..., example="Desctription")
    value: float = Field(..., example=0.0)
    currency: accounts.CurrencyEnum = Field(..., example=accounts.CurrencyEnum.THB)


class Transaction(bases.BaseSchema, BaseTransaction):
    from_account_book: account_books.ReferenceAccountBook
    to_account_book: account_books.ReferenceAccountBook
    creator: users.ReferenceUser
    updated_by: users.ReferenceUser

    status: str = Field(
        default="active",
        example="active",
    )


class TransactionList(BaseModel):
    transactions: list[Transaction]


class CreatedTransaction(BaseTransaction):
    from_account_book_id: str = Field(..., example="0")
    to_account_book_id: str = Field(..., example="0")
