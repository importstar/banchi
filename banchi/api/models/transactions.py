from banchi.api import schemas
from typing import Optional

from beanie import Document, Indexed, Link, PydanticObjectId, DecimalAnnotation
from pydantic import Field

from . import users
from . import spaces
from . import accounts
from . import account_books

import datetime


class TransactionDocument(Document):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId,
        alias="_id",
    )

    file_id: PydanticObjectId | None = Field(
        default_factory=PydanticObjectId,
    )
    transaction: Link["Transaction"]
    description: Optional[str] = None

    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    creator: Link[users.User]
    updated_by: Link[users.User]

    class Settings:
        name = "transaction_documents"


class Transaction(schemas.transactions.Transaction, Document):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId,
        alias="_id",
    )
    from_account_book: Link[account_books.AccountBook]
    to_account_book: Link[account_books.AccountBook]
    value: DecimalAnnotation

    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    creator: Link[users.User]
    updated_by: Link[users.User]

    # files: list[Link[TransactionDocument]]

    class Settings:
        name = "transactions"


class TransactionTemplate(schemas.transactions.TransactionTemplate, Document):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId,
        alias="_id",
    )
    transactions: Transaction

    creator: Link[users.User]
    updated_by: Link[users.User]

    created_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)

    class Settings:
        name = "transaction_templates"
