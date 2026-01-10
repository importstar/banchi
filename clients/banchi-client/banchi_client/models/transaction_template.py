from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference_account import ReferenceAccount
    from ..models.reference_user import ReferenceUser
    from ..models.transaction import Transaction


T = TypeVar("T", bound="TransactionTemplate")


@_attrs_define
class TransactionTemplate:
    """
    Attributes:
        transactions (list[Transaction]):
        name (str):  Example: Transaction Template Name.
        account (ReferenceAccount):
        creator (ReferenceUser):
        updated_by (ReferenceUser):
        status (str | Unset):  Default: 'active'. Example: active.
    """

    transactions: list[Transaction]
    name: str
    account: ReferenceAccount
    creator: ReferenceUser
    updated_by: ReferenceUser
    status: str | Unset = "active"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transactions = []
        for transactions_item_data in self.transactions:
            transactions_item = transactions_item_data.to_dict()
            transactions.append(transactions_item)

        name = self.name

        account = self.account.to_dict()

        creator = self.creator.to_dict()

        updated_by = self.updated_by.to_dict()

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transactions": transactions,
                "name": name,
                "account": account,
                "creator": creator,
                "updated_by": updated_by,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reference_account import ReferenceAccount
        from ..models.reference_user import ReferenceUser
        from ..models.transaction import Transaction

        d = dict(src_dict)
        transactions = []
        _transactions = d.pop("transactions")
        for transactions_item_data in _transactions:
            transactions_item = Transaction.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        name = d.pop("name")

        account = ReferenceAccount.from_dict(d.pop("account"))

        creator = ReferenceUser.from_dict(d.pop("creator"))

        updated_by = ReferenceUser.from_dict(d.pop("updated_by"))

        status = d.pop("status", UNSET)

        transaction_template = cls(
            transactions=transactions,
            name=name,
            account=account,
            creator=creator,
            updated_by=updated_by,
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
