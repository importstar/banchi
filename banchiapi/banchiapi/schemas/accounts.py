from bson import ObjectId

import enum
from pydantic import BaseModel, Field
from beanie import PydanticObjectId

from . import users
from . import spaces
from .system_settings import BaseAuthorizedSignatory


class CurrencyEnum(str, enum.Enum):
    THB = "THB"


class BaseAccount(BaseModel):
    name: str = Field(..., example="Account Name")
    description: str = Field(..., example="Description")

    currency: CurrencyEnum = Field(..., example=CurrencyEnum.THB)


class Account(BaseAccount):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId, alias="_id", example="0"
    )

    spaces: list[spaces.Space]
    creator: list[users.User]


class CreatedAccount(BaseAccount):
    space_id: str = Field(..., example="0")


class AccountList(BaseModel):
    accounts: list[Account]
