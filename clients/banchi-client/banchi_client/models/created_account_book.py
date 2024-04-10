from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_type_enum import AccountTypeEnum
from ..models.currency_enum import CurrencyEnum
from ..models.smallest_fraction_enum import SmallestFractionEnum
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
        type (Union[Unset, AccountTypeEnum]):  Default: AccountTypeEnum.ASSET.
        smallest_fraction (Union[Unset, SmallestFractionEnum]):  Default: SmallestFractionEnum.VALUE_100.
        currency (Union[Unset, CurrencyEnum]):  Default: CurrencyEnum.THB.
    """

    name: str
    parent_id: Union[None, str]
    account_id: str
    description: Union[Unset, str] = ""
    type: Union[Unset, AccountTypeEnum] = AccountTypeEnum.ASSET
    smallest_fraction: Union[Unset, SmallestFractionEnum] = SmallestFractionEnum.VALUE_100
    currency: Union[Unset, CurrencyEnum] = CurrencyEnum.THB
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        parent_id: Union[None, str]
        parent_id = self.parent_id

        account_id = self.account_id

        description = self.description

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        smallest_fraction: Union[Unset, int] = UNSET
        if not isinstance(self.smallest_fraction, Unset):
            smallest_fraction = self.smallest_fraction.value

        currency: Union[Unset, str] = UNSET
        if not isinstance(self.currency, Unset):
            currency = self.currency.value

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

        _type = d.pop("type", UNSET)
        type: Union[Unset, AccountTypeEnum]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = AccountTypeEnum(_type)

        _smallest_fraction = d.pop("smallest_fraction", UNSET)
        smallest_fraction: Union[Unset, SmallestFractionEnum]
        if isinstance(_smallest_fraction, Unset):
            smallest_fraction = UNSET
        else:
            smallest_fraction = SmallestFractionEnum(_smallest_fraction)

        _currency = d.pop("currency", UNSET)
        currency: Union[Unset, CurrencyEnum]
        if isinstance(_currency, Unset):
            currency = UNSET
        else:
            currency = CurrencyEnum(_currency)

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
