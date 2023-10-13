from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreatedAccountBook")


@_attrs_define
class CreatedAccountBook:
    """
    Attributes:
        name (str):  Example: Account Name.
        description (str):  Example: Description.
        type (str):  Example: asset.
        currency (str):
        parent_id (Union[None, str]):
        account_id (str):  Example: 0.
    """

    name: str
    description: str
    type: str
    currency: str
    parent_id: Union[None, str]
    account_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        type = self.type
        currency = self.currency
        parent_id: Union[None, str]

        parent_id = self.parent_id

        account_id = self.account_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "type": type,
                "currency": currency,
                "parent_id": parent_id,
                "account_id": account_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        type = d.pop("type")

        currency = d.pop("currency")

        def _parse_parent_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        account_id = d.pop("account_id")

        created_account_book = cls(
            name=name,
            description=description,
            type=type,
            currency=currency,
            parent_id=parent_id,
            account_id=account_id,
        )

        created_account_book.additional_properties = d
        return created_account_book

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
