from banchiapi import schemas
from typing import Optional

from beanie import Document, Indexed, Link
from pydantic import Field

from . import users

import datetime


class AccountBook(schemas.account_books.AccountBook, Document):
    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    owner: Link[users.User]
    updated_by: Link[users.User]

    class Settings:
        name = "account_books"
