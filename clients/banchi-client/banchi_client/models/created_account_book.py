from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

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
        type_ (Union[Unset, AccountTypeEnum]):
        smallest_fraction (Union[Unset, SmallestFractionEnum]):
        currency (Union[Unset, CurrencyEnum]):
    """

    name: str
    parent_id: Union[None, str]
    account_id: str
    description: Union[Unset, str] = ""
    type_: Union[Unset, AccountTypeEnum] = UNSET
    smallest_fraction: Union[Unset, SmallestFractionEnum] = UNSET
    currency: Union[Unset, CurrencyEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        parent_id: Union[None, str]
        parent_id = self.parent_id

        account_id = self.account_id

        description = self.description

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        smallest_fraction: Union[Unset, int] = UNSET
        if not isinstance(self.smallest_fraction, Unset):
            smallest_fraction = self.smallest_fraction.value

        currency: Union[Unset, str] = UNSET
        if not isinstance(self.currency, Unset):
            currency = self.currency.value

        field_dict: dict[str, Any] = {}
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
        if type_ is not UNSET:
            field_dict["type"] = type_
        if smallest_fraction is not UNSET:
            field_dict["smallest_fraction"] = smallest_fraction
        if currency is not UNSET:
            field_dict["currency"] = currency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_parent_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        account_id = d.pop("account_id")

        description = d.pop("description", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, AccountTypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = AccountTypeEnum(_type_)

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
            type_=type_,
            smallest_fraction=smallest_fraction,
            currency=currency,
        )

        created_account_book.additional_properties = d
        return created_account_book

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
