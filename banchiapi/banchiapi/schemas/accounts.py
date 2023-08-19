from bson import ObjectId

from pydantic import BaseModel, Field

from .base import BaseEmbeddedSchema, BaseSchema, PyObjectId
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


class BaseAccount(BaseModel):
    name: str = Field(..., example="Account Name")
    type: str = Field(..., example="asset")
    smallest_fraction: float = Field(..., example=0.1)
    parent_id: str = Field(..., example="parent_id")
    currency: str = Field(..., example="THB")


class Account(BaseSchema, BaseAccount):
    pass


class CreatedAccount(BaseAccount):
    pass
