from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_type_enum import AccountTypeEnum

T = TypeVar("T", bound="ReferenceAccountBook")


@_attrs_define
class ReferenceAccountBook:
    """
    Attributes:
        id (str):  Example: 0.
        name (str):  Example: Account Book Name.
        type (AccountTypeEnum):
    """

    id: str
    name: str
    type: AccountTypeEnum
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        type = AccountTypeEnum(d.pop("type"))

        reference_account_book = cls(
            id=id,
            name=name,
            type=type,
        )

        reference_account_book.additional_properties = d
        return reference_account_book

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
