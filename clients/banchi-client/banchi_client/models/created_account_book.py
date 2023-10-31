from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.account_type_enum import AccountTypeEnum
from ..models.smallest_fraction_enum import SmallestFractionEnum
from ..models.currency_enum import CurrencyEnum
from typing import cast, Union


T = TypeVar("T", bound="CreatedAccountBook")


@_attrs_define
class CreatedAccountBook:
    """
    Attributes:
        name (str):  Example: Account Name.
        description (str):  Example: Description.
        type (AccountTypeEnum):
        smallest_fraction (SmallestFractionEnum):
        currency (CurrencyEnum):
        parent_id (Union[None, str]):
        account_id (str):  Example: 0.
    """

    name: str
    description: str
    type: AccountTypeEnum
    smallest_fraction: SmallestFractionEnum
    currency: CurrencyEnum
    parent_id: Union[None, str]
    account_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        type = self.type.value

        smallest_fraction = self.smallest_fraction.value

        currency = self.currency.value

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
                "smallest_fraction": smallest_fraction,
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

        type = AccountTypeEnum(d.pop("type"))

        smallest_fraction = SmallestFractionEnum(d.pop("smallest_fraction"))

        currency = CurrencyEnum(d.pop("currency"))

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
            smallest_fraction=smallest_fraction,
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
