from bson import ObjectId
import datetime
import decimal

from pydantic import BaseModel, Field
from beanie import PydanticObjectId

import typing

from . import account_books
from . import accounts
from . import spaces
from . import users
from . import bases


class BaseTransaction(BaseModel):
    date: datetime.datetime = datetime.datetime.now()
    description: str = Field(..., example="Desctription")
    value: decimal.Decimal = Field(..., example=0.0, decimal_places=2)
    currency: accounts.CurrencyEnum = Field(..., example=accounts.CurrencyEnum.THB)
    tags: list[str] = Field(default=[])

    remarks: str | None = Field(default="", example="Text Remark")


class Transaction(bases.BaseSchema, BaseTransaction):

    from_account_book: account_books.ReferenceAccountBook
    to_account_book: account_books.ReferenceAccountBook

    creator: users.ReferenceUser
    updated_by: users.ReferenceUser

    status: str = Field(
        default="active",
        example="active",
    )

    created_date: datetime.datetime
    updated_date: datetime.datetime


class TransactionList(BaseModel):
    transactions: list[Transaction]
    page: int = 1
    size_per_page: int = 50
    page_size: int = 1


class CreatedTransaction(BaseTransaction):
    from_account_book_id: PydanticObjectId = Field(..., example="0")
    to_account_book_id: PydanticObjectId = Field(..., example="0")


class UpdatedTransaction(CreatedTransaction):
    pass


class TransactionInfo(CreatedTransaction):
    pass


class CreatedTransactionInfo(TransactionInfo):
    pass


class BaseTransactionTemplate(BaseModel):
    name: str = Field(..., example="Transaction Template Name")
    transactions: list[TransactionInfo]


class TransactionTemplate(BaseTransactionTemplate, bases.BaseSchema):

    account: accounts.ReferenceAccount
    creator: users.ReferenceUser
    updated_by: users.ReferenceUser

    status: str = Field(
        default="active",
        example="active",
    )

    created_date: datetime.datetime
    updated_date: datetime.datetime


class TransactionTemplateList(bases.BaseSchemaList):
    transaction_templates: list[TransactionTemplate]


class CreatedTransactionTemplate(BaseTransactionTemplate):
    transactions: list[CreatedTransactionInfo]


class UpdatedTransactionTemplate(CreatedTransactionTemplate):
    pass
