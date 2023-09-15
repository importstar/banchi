from banchiapi import schemas
from typing import Optional

from beanie import Document, Indexed, Link
from pydantic import Field

from . import users
from . import spaces
from . import accounts
from . import account_books

import datetime


class Transaction(schemas.transactions.Transaction, Document):
    account_book: Link[account_books.AccountBook]

    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    owner: Link[users.User]
    updated_by: Link[users.User]

    class Settings:
        name = "transactions"
