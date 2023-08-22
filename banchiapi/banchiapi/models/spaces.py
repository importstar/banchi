from banchiapi import schemas

from beanie import Document, Indexed
from pydantic import Field

from . import users

import datetime


class Space(schemas.spaces.Space, Document):
    created_date: datetime.datetime = Field(default=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default=datetime.datetime.now)
    owner: users.User

    class Settings:
        name = "spaces"
