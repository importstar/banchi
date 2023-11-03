from bson import ObjectId

import enum
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
    liability = "liability"
    stock = "stock"
    multual_fund = "multual fund"


# smallest_fractions = [1.0, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]


class SmallestFractionEnum(int, enum.Enum):
    f1 = 1
    f0_1 = 10
    f0_01 = 100
    f0_001 = 1000
    f0_0001 = 10000
    f0_00001 = 100000
    f0_000001 = 1000000


class BaseAccountBook(BaseModel):
    name: str = Field(..., example="Account Book Name")
    description: str = Field(..., example="Description")
    type: AccountTypeEnum = Field(
        ...,
        example=AccountTypeEnum.asset,
    )
    smallest_fraction: SmallestFractionEnum = Field(
        ..., example=SmallestFractionEnum.f0_01
    )
    currency: accounts.CurrencyEnum = Field(..., example=accounts.CurrencyEnum.THB)


class AccountBook(bases.BaseSchema, BaseAccountBook):
    account: accounts.Account
    creator: users.User

    status: str = Field(
        default="active",
        example="active",
    )


class ReferenceAccountBook(bases.BaseSchema):
    name: str = Field(..., example="Account Book Name")


class CreatedAccountBook(BaseAccountBook):
    parent_id: str | None = Field(..., example=None)
    account_id: str = Field(..., example="0")


class AccountBookList(BaseModel):
    account_books: list[AccountBook]
