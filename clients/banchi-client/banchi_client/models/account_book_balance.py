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
        balance (str):
        increase (str):
        decrease (str):
        net_balance (str):
        net_increase (str):
        net_decrease (str):
        children (Union[Unset, int]):  Default: 0.
        type_ (Union[Unset, AccountTypeEnum]):
    """

    id: str
    balance: str
    increase: str
    decrease: str
    net_balance: str
    net_increase: str
    net_decrease: str
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
                "balance": balance,
                "increase": increase,
                "decrease": decrease,
                "net_balance": net_balance,
                "net_increase": net_increase,
                "net_decrease": net_decrease,
            }
        )
        if children is not UNSET:
            field_dict["children"] = children
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        balance = d.pop("balance")

        increase = d.pop("increase")

        decrease = d.pop("decrease")

        net_balance = d.pop("net_balance")

        net_increase = d.pop("net_increase")

        net_decrease = d.pop("net_decrease")

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
