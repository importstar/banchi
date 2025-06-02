from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_type_enum import AccountTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountBookBalance")


@_attrs_define
class AccountBookBalance:
    """
    Attributes:
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        balance (Union[Unset, str]):  Default: '0'.
        increase (Union[Unset, str]):  Default: '0'.
        decrease (Union[Unset, str]):  Default: '0'.
        net_balance (Union[Unset, str]):  Default: '0'.
        net_increase (Union[Unset, str]):  Default: '0'.
        net_decrease (Union[Unset, str]):  Default: '0'.
        children (Union[Unset, int]):  Default: 0.
        type_ (Union[Unset, AccountTypeEnum]):
    """

    id: str
    balance: Union[Unset, str] = "0"
    increase: Union[Unset, str] = "0"
    decrease: Union[Unset, str] = "0"
    net_balance: Union[Unset, str] = "0"
    net_increase: Union[Unset, str] = "0"
    net_decrease: Union[Unset, str] = "0"
    children: Union[Unset, int] = 0
    type_: Union[Unset, AccountTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        balance = self.balance

        increase = self.increase

        decrease = self.decrease

        net_balance = self.net_balance

        net_increase = self.net_increase

        net_decrease = self.net_decrease

        children = self.children

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if balance is not UNSET:
            field_dict["balance"] = balance
        if increase is not UNSET:
            field_dict["increase"] = increase
        if decrease is not UNSET:
            field_dict["decrease"] = decrease
        if net_balance is not UNSET:
            field_dict["net_balance"] = net_balance
        if net_increase is not UNSET:
            field_dict["net_increase"] = net_increase
        if net_decrease is not UNSET:
            field_dict["net_decrease"] = net_decrease
        if children is not UNSET:
            field_dict["children"] = children
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        balance = d.pop("balance", UNSET)

        increase = d.pop("increase", UNSET)

        decrease = d.pop("decrease", UNSET)

        net_balance = d.pop("net_balance", UNSET)

        net_increase = d.pop("net_increase", UNSET)

        net_decrease = d.pop("net_decrease", UNSET)

        children = d.pop("children", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, AccountTypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = AccountTypeEnum(_type_)

        account_book_balance = cls(
            id=id,
            balance=balance,
            increase=increase,
            decrease=decrease,
            net_balance=net_balance,
            net_increase=net_increase,
            net_decrease=net_decrease,
            children=children,
            type_=type_,
        )

        account_book_balance.additional_properties = d
        return account_book_balance

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
