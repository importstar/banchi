from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_book_summary import AccountBookSummary


T = TypeVar("T", bound="AccountBookSummaryList")


@_attrs_define
class AccountBookSummaryList:
    """
    Attributes:
        account_book_summaries (list[AccountBookSummary]):
    """

    account_book_summaries: list[AccountBookSummary]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_book_summaries = []
        for account_book_summaries_item_data in self.account_book_summaries:
            account_book_summaries_item = account_book_summaries_item_data.to_dict()
            account_book_summaries.append(account_book_summaries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_book_summaries": account_book_summaries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_book_summary import AccountBookSummary

        d = dict(src_dict)
        account_book_summaries = []
        _account_book_summaries = d.pop("account_book_summaries")
        for account_book_summaries_item_data in _account_book_summaries:
            account_book_summaries_item = AccountBookSummary.from_dict(account_book_summaries_item_data)

            account_book_summaries.append(account_book_summaries_item)

        account_book_summary_list = cls(
            account_book_summaries=account_book_summaries,
        )

        account_book_summary_list.additional_properties = d
        return account_book_summary_list

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
