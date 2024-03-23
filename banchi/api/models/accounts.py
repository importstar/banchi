from banchi.api import schemas
from typing import Optional

from beanie import Document, Indexed, Link, PydanticObjectId
from pydantic import Field

from . import users
from . import spaces

import datetime


class Account(schemas.accounts.Account, Document):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId,
        alias="_id",
    )

    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    space: Link[spaces.Space]
    creator: Link[users.User]
    updated_by: Link[users.User]

    class Settings:
        name = "accounts"
