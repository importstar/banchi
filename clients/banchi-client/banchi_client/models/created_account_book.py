from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatedAccountBook")


@_attrs_define
class CreatedAccountBook:
    """
    Attributes:
        name (str):  Example: Account Book Name.
        parent_id (Union[None, str]):
        account_id (str):  Example: 0.
        description (Union[Unset, str]):  Default: ''. Example: Description.
        type (Union[Unset, Any]):  Default: 'asset'. Example: asset.
        smallest_fraction (Union[Unset, Any]):  Default: 100. Example: 100.
        currency (Union[Unset, Any]):  Default: 'THB'. Example: THB.
    """

    name: str
    parent_id: Union[None, str]
    account_id: str
    description: Union[Unset, str] = ""
    type: Union[Unset, Any] = "asset"
    smallest_fraction: Union[Unset, Any] = 100
    currency: Union[Unset, Any] = "THB"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        parent_id: Union[None, str]
        parent_id = self.parent_id

        account_id = self.account_id

        description = self.description

        type = self.type

        smallest_fraction = self.smallest_fraction

        currency = self.currency

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "parent_id": parent_id,
                "account_id": account_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type
        if smallest_fraction is not UNSET:
            field_dict["smallest_fraction"] = smallest_fraction
        if currency is not UNSET:
            field_dict["currency"] = currency

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        def _parse_parent_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        account_id = d.pop("account_id")

        description = d.pop("description", UNSET)

        type = d.pop("type", UNSET)

        smallest_fraction = d.pop("smallest_fraction", UNSET)

        currency = d.pop("currency", UNSET)

        created_account_book = cls(
            name=name,
            parent_id=parent_id,
            account_id=account_id,
            description=description,
            type=type,
            smallest_fraction=smallest_fraction,
            currency=currency,
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
