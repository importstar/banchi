from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.currency_enum import CurrencyEnum

T = TypeVar("T", bound="CreatedAccount")


@_attrs_define
class CreatedAccount:
    """
    Attributes:
        name (str):  Example: Account Name.
        description (str):  Example: Description.
        currency (CurrencyEnum):
        space_id (str):  Example: 0.
    """

    name: str
    description: str
    currency: CurrencyEnum
    space_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        currency = self.currency.value

        space_id = self.space_id

        field_dict: Dict[str, Any] = {}
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        currency = CurrencyEnum(d.pop("currency"))

        space_id = d.pop("space_id")

        created_account = cls(
            name=name,
            description=description,
            currency=currency,
            space_id=space_id,
        )

        created_account.additional_properties = d
        return created_account

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
