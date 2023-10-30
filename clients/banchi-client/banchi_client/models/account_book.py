from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union


T = TypeVar("T", bound="AccountBook")


@_attrs_define
class AccountBook:
    """
    Attributes:
        name (str):  Example: Account Name.
        description (str):  Example: Description.
        type (str):  Example: asset.
        currency (str):
        field_id (Union[Unset, str]):  Example: 0.
    """

    name: str
    description: str
    type: str
    currency: str
    field_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        type = self.type
        currency = self.currency
        field_id = self.field_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "type": type,
                "currency": currency,
            }
        )
        if field_id is not UNSET:
            field_dict["_id"] = field_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        type = d.pop("type")

        currency = d.pop("currency")

        field_id = d.pop("_id", UNSET)

        account_book = cls(
            name=name,
            description=description,
            type=type,
            currency=currency,
            field_id=field_id,
        )

        account_book.additional_properties = d
        return account_book

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
