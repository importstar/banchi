from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference_account import ReferenceAccount
    from ..models.reference_user import ReferenceUser
    from ..models.transaction_info import TransactionInfo


T = TypeVar("T", bound="TransactionTemplate")


@_attrs_define
class TransactionTemplate:
    """
    Attributes:
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        name (str):  Example: Transaction Template Name.
        transactions (list[TransactionInfo]):
        account (ReferenceAccount):
        creator (ReferenceUser):
        updated_by (ReferenceUser):
        created_date (datetime.datetime):
        updated_date (datetime.datetime):
        status (str | Unset):  Default: 'active'. Example: active.
    """

    id: str
    name: str
    transactions: list[TransactionInfo]
    account: ReferenceAccount
    creator: ReferenceUser
    updated_by: ReferenceUser
    created_date: datetime.datetime
    updated_date: datetime.datetime
    status: str | Unset = "active"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        transactions = []
        for transactions_item_data in self.transactions:
            transactions_item = transactions_item_data.to_dict()
            transactions.append(transactions_item)

        account = self.account.to_dict()

        creator = self.creator.to_dict()

        updated_by = self.updated_by.to_dict()

        created_date = self.created_date.isoformat()

        updated_date = self.updated_date.isoformat()

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "transactions": transactions,
                "account": account,
                "creator": creator,
                "updated_by": updated_by,
                "created_date": created_date,
                "updated_date": updated_date,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reference_account import ReferenceAccount
        from ..models.reference_user import ReferenceUser
        from ..models.transaction_info import TransactionInfo

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        transactions = []
        _transactions = d.pop("transactions")
        for transactions_item_data in _transactions:
            transactions_item = TransactionInfo.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        account = ReferenceAccount.from_dict(d.pop("account"))

        creator = ReferenceUser.from_dict(d.pop("creator"))

        updated_by = ReferenceUser.from_dict(d.pop("updated_by"))

        created_date = isoparse(d.pop("created_date"))

        updated_date = isoparse(d.pop("updated_date"))

        status = d.pop("status", UNSET)

        transaction_template = cls(
            id=id,
            name=name,
            transactions=transactions,
            account=account,
            creator=creator,
            updated_by=updated_by,
            created_date=created_date,
            updated_date=updated_date,
            status=status,
        )

        transaction_template.additional_properties = d
        return transaction_template

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
