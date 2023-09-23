from bson import ObjectId

import enum
from pydantic import BaseModel, Field
from beanie import PydanticObjectId

from .accounts import CurrencyEnum

account_types = [
    "asset",
    "bank",
    "cash",
    "credit card",
    "liability",
    "stock",
    "multual fund",
]

smallest_fractions = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]


class SmallestFractionEnum(float, enum.Enum):
    f1 = 1
    f0_1 = 0.1
    f0_01 = 0.01
    f0_001 = 0.001
    f0_0001 = 0.0001
    f0_00001 = 0.00001
    f0_000001 = 0.000001


class BaseAccountBook(BaseModel):
    name: str = Field(..., example="Account Name")
    description: str = Field(..., example="Description")
    type: str = Field(
        ...,
        example="asset",
    )
    smallest_fraction: SmallestFractionEnum = Field(
        ..., example=SmallestFractionEnum.f0_01
    )
    currency: CurrencyEnum = Field(..., example=CurrencyEnum.THB)


class AccountBook(BaseAccountBook):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId, alias="_id", example="0"
    )


class CreatedAccountBook(BaseAccountBook):
    parent_id: str | None = Field(..., example=None)
    account_id: str = Field(..., example="0")


class AccountBookList(BaseModel):
    account_books: list[AccountBook]
