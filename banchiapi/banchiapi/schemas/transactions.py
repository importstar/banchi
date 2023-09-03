from bson import ObjectId

from pydantic import BaseModel, Field

from .base import BaseEmbeddedSchema, BaseSchema, PyObjectId

from . import accounts
from . import spaces


class BaseTransaction(BaseModel):
    desctiption: str = Field(..., example="Desctription")
    value: str = Field(..., example="0")
    currency: accounts.CurrencyEnum = Field(..., example=accounts.CurrencyEnum.THB)


class Transaction(BaseSchema, BaseTransaction):
    transaction_id: str = Field(..., example="0")
    account: accounts.Account = Field(..., example="0")
    sapce: spaces.Space = Field(..., example="0")
    status: str = Field(
        default="active",
        example="active",
    )


class TransactionList(BaseSchema):
    spaces: list[Transaction]


class CreatedTransaction(BaseTransaction):
    account_id: str = Field(..., example="0")
    sapce_id: str = Field(..., example="0")
