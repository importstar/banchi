from bson import ObjectId

from pydantic import BaseModel, Field
from beanie import PydanticObjectId

from . import account_books
from . import accounts
from . import spaces


class BaseTransaction(BaseModel):
    desctiption: str = Field(..., example="Desctription")
    value: str = Field(..., example="0")
    currency: accounts.CurrencyEnum = Field(..., example=accounts.CurrencyEnum.THB)


class Transaction(BaseTransaction):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId, alias="_id", example="0"
    )

    account_book: account_books.AccountBook = Field(..., example="0")
    status: str = Field(
        default="active",
        example="active",
    )


class TransactionList(BaseModel):
    spaces: list[Transaction]


class CreatedTransaction(BaseTransaction):
    account_id: str = Field(..., example="0")
    sapce_id: str = Field(..., example="0")
