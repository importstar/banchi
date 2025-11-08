from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountBookLabel")


@_attrs_define
class AccountBookLabel:
    """
    Attributes:
        positive (str | Unset):  Default: 'increase'. Example: increase.
        negative (str | Unset):  Default: 'decrease'. Example: decrease.
    """

    positive: str | Unset = "increase"
    negative: str | Unset = "decrease"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        positive = self.positive

        negative = self.negative

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if positive is not UNSET:
            field_dict["positive"] = positive
        if negative is not UNSET:
            field_dict["negative"] = negative

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        positive = d.pop("positive", UNSET)

        negative = d.pop("negative", UNSET)

        account_book_label = cls(
            positive=positive,
            negative=negative,
        )

        account_book_label.additional_properties = d
        return account_book_label

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
