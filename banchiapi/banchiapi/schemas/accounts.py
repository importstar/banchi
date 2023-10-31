from bson import ObjectId

import enum
from pydantic import BaseModel, Field
from beanie import PydanticObjectId

from . import users
from . import spaces
from . import bases
from .system_settings import BaseAuthorizedSignatory


class CurrencyEnum(str, enum.Enum):
    THB = "THB"
    USD = "USD"


class BaseAccount(BaseModel):
    name: str = Field(..., example="Account Name")
    description: str = Field(..., example="Description")

    currency: CurrencyEnum = Field(..., example=CurrencyEnum.THB)


class Account(bases.BaseSchema, BaseAccount):
    space: spaces.Space
    creator: users.User

    status: str = Field(
        default="active",
        example="active",
    )


class CreatedAccount(BaseAccount):
    space_id: str = Field(..., example="0")


class AccountList(BaseModel):
    accounts: list[Account]
