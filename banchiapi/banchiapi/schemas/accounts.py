from bson import ObjectId

import enum
from pydantic import BaseModel, Field

from .base import BaseEmbeddedSchema, BaseSchema
from .system_settings import BaseAuthorizedSignatory

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


class BaseAccount(BaseModel):
    name: str = Field(..., example="Account Name")
    type: str = Field(
        ...,
        example="asset",
    )
    smallest_fraction: SmallestFractionEnum = Field(
        ..., example=SmallestFractionEnum.f0_01
    )
    parent_id: str = Field(..., example="parent_id")
    currency: str = Field(..., example="THB")


class Account(BaseSchema, BaseAccount):
    pass


class CreatedAccount(BaseAccount):
    parent_id: str = Field(..., example="null")
    space_id: str = Field(..., example="0")


class AccountList(BaseSchema):
    accounts: list[Account]
