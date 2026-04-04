from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transaction import Transaction


T = TypeVar("T", bound="TransactionList")


@_attrs_define
class TransactionList:
    """
    Attributes:
        transactions (list[Transaction]):
        page (int | Unset):  Default: 1.
        size_per_page (int | Unset):  Default: 50.
        page_size (int | Unset):  Default: 1.
    """

    transactions: list[Transaction]
    page: int | Unset = 1
    size_per_page: int | Unset = 50
    page_size: int | Unset = 1
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transactions = []
        for transactions_item_data in self.transactions:
            transactions_item = transactions_item_data.to_dict()
            transactions.append(transactions_item)

        page = self.page

        size_per_page = self.size_per_page

        page_size = self.page_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transactions": transactions,
            }
        )
        if page is not UNSET:
            field_dict["page"] = page
        if size_per_page is not UNSET:
            field_dict["size_per_page"] = size_per_page
        if page_size is not UNSET:
            field_dict["page_size"] = page_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transaction import Transaction

        d = dict(src_dict)
        transactions = []
        _transactions = d.pop("transactions")
        for transactions_item_data in _transactions:
            transactions_item = Transaction.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        page = d.pop("page", UNSET)

        size_per_page = d.pop("size_per_page", UNSET)

        page_size = d.pop("page_size", UNSET)

        transaction_list = cls(
            transactions=transactions,
            page=page,
            size_per_page=size_per_page,
            page_size=page_size,
        )

        transaction_list.additional_properties = d
        return transaction_list

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
