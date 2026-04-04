from banchi.api import schemas
from typing import Optional

from beanie import (
    Document,
    Indexed,
    Link,
    PydanticObjectId,
    BackLink,
    DecimalAnnotation,
)
from pydantic import Field

from . import users
from . import accounts

import datetime


class AccountBook(schemas.account_books.AccountBook, Document):
    class Settings:
        name = "account_books"

    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId,
        alias="_id",
    )

    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)

    account: Link[accounts.Account]
    parent: Optional[Link["AccountBook"]] = None

    creator: Link[users.User]
    updated_by: Link[users.User]

    balance: DecimalAnnotation = 0
    # increase: DecimalAnnotation = 0
    # decrease: DecimalAnnotation = 0

    children: list[BackLink["AccountBook"]] = Field(original_field="parent")


class AccountBookSummary(schemas.account_books.AccountBookSummary, Document):
    class Settings:
        name = "account_book_summaries"

    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId,
        alias="_id",
    )

    increase: DecimalAnnotation = 0
    decrease: DecimalAnnotation = 0
    balance: DecimalAnnotation = 0

    account_book: Link["AccountBook"]

    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
