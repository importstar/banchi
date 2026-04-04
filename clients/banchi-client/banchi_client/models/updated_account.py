from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.currency_enum import CurrencyEnum

T = TypeVar("T", bound="UpdatedAccount")


@_attrs_define
class UpdatedAccount:
    """
    Attributes:
        name (str):  Example: Account Name.
        description (str):  Example: Description.
        currency (CurrencyEnum):
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
    """

    name: str
    description: str
    currency: CurrencyEnum
    space_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        currency = self.currency.value

        space_id = self.space_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "currency": currency,
                "space_id": space_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        currency = CurrencyEnum(d.pop("currency"))

        space_id = d.pop("space_id")

        updated_account = cls(
            name=name,
            description=description,
            currency=currency,
            space_id=space_id,
        )

        updated_account.additional_properties = d
        return updated_account

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
