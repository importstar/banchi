from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.created_transaction_info import CreatedTransactionInfo


T = TypeVar("T", bound="CreatedTransactionTemplate")


@_attrs_define
class CreatedTransactionTemplate:
    """
    Attributes:
        name (str):  Example: Transaction Template Name.
        transactions (list[CreatedTransactionInfo]):
    """

    name: str
    transactions: list[CreatedTransactionInfo]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        transactions = []
        for transactions_item_data in self.transactions:
            transactions_item = transactions_item_data.to_dict()
            transactions.append(transactions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "transactions": transactions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.created_transaction_info import CreatedTransactionInfo

        d = dict(src_dict)
        name = d.pop("name")

        transactions = []
        _transactions = d.pop("transactions")
        for transactions_item_data in _transactions:
            transactions_item = CreatedTransactionInfo.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        created_transaction_template = cls(
            name=name,
            transactions=transactions,
        )

        created_transaction_template.additional_properties = d
        return created_transaction_template

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
