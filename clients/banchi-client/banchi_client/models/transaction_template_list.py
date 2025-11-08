from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TransactionTemplateList")


@_attrs_define
class TransactionTemplateList:
    """
    Attributes:
        page (int | Unset):  Default: 1.
        size_per_page (int | Unset):  Default: 50.
        page_size (int | Unset):  Default: 1.
    """

    page: int | Unset = 1
    size_per_page: int | Unset = 50
    page_size: int | Unset = 1
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page = self.page

        size_per_page = self.size_per_page

        page_size = self.page_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page is not UNSET:
            field_dict["page"] = page
        if size_per_page is not UNSET:
            field_dict["size_per_page"] = size_per_page
        if page_size is not UNSET:
            field_dict["page_size"] = page_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        page = d.pop("page", UNSET)

        size_per_page = d.pop("size_per_page", UNSET)

        page_size = d.pop("page_size", UNSET)

        transaction_template_list = cls(
            page=page,
            size_per_page=size_per_page,
            page_size=page_size,
        )

        transaction_template_list.additional_properties = d
        return transaction_template_list

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
