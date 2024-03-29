from banchi.api import schemas
from typing import Optional

from beanie import Document, Indexed, Link, PydanticObjectId
from pydantic import Field

from . import users

import datetime


class Space(schemas.spaces.Space, Document):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId,
        alias="_id",
    )

    name: str
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    owner: Link[users.User]
    updated_by: Link[users.User]

    class Settings:
        name = "spaces"


class SpaceRole(schemas.spaces.SpaceRole, Document):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId,
        alias="_id",
    )

    added_by: Link[users.User]
    member: Link[users.User]
    updated_by: Link[users.User]
    space: Link[Space]

    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)

    class Settings:
        name = "space_roles"
