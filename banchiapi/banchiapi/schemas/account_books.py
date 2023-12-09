from bson import ObjectId

import enum
import decimal
import typing
from pydantic import BaseModel, Field

from beanie import PydanticObjectId

from . import bases
from . import users
from . import accounts


class AccountTypeEnum(str, enum.Enum):
    asset = "asset"
    bank = "bank"
    cash = "cash"
    credit_card = "credit card"
    expense = "expense"
    equity = "equity"
    income = "income"
    liability = "liability"
    stock = "stock"
    multual_fund = "multual fund"
    trading = "trading"


class SmallestFractionEnum(int, enum.Enum):
    f1 = 1
    f0_1 = 10
    f0_01 = 100
    f0_001 = 1000
    f0_0001 = 10000
    f0_00001 = 100000
    f0_000001 = 1000000


class AccountBookBalance(BaseModel):
    balance: decimal.Decimal
    increse: decimal.Decimal
    decrese: decimal.Decimal


class BaseAccountBook(BaseModel):
    name: str = Field(..., example="Account Book Name")
    description: str = Field(default="", example="Description")
    type: AccountTypeEnum = Field(
        default=AccountTypeEnum.asset,
        example=AccountTypeEnum.asset,
    )
    smallest_fraction: SmallestFractionEnum = Field(
        default=SmallestFractionEnum.f0_01, example=SmallestFractionEnum.f0_01
    )
    currency: accounts.CurrencyEnum = Field(
        default=accounts.CurrencyEnum.THB, example=accounts.CurrencyEnum.THB
    )


class ReferenceAccountBook(bases.BaseSchema):
    name: str = Field(..., example="Account Book Name")
    parent: typing.Annotated["ReferenceAccountBook", ...] | None


class AccountBook(bases.BaseSchema, BaseAccountBook):
    account: accounts.ReferenceAccount
    parent: ReferenceAccountBook | None
    creator: users.ReferenceUser
    display_name: str | None

    status: str = Field(
        default="active",
        example="active",
    )


class AccountBookLabel(BaseModel):
    positive: str = Field(default="increase", example="increase")
    negative: str = Field(default="decrease", example="decrease")


class CreatedAccountBook(BaseAccountBook):
    parent_id: str | None = Field(..., example=None)
    account_id: str = Field(..., example="0")


class AccountBookList(BaseModel):
    account_books: list[AccountBook]
