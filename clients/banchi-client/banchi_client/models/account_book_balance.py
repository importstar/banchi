from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountBookBalance")


@_attrs_define
class AccountBookBalance:
    """
    Attributes:
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        balance (Union[Unset, str]):
        increse (Union[Unset, str]):
        decrese (Union[Unset, str]):
        net_balance (Union[Unset, str]):
        net_increse (Union[Unset, str]):
        net_decrese (Union[Unset, str]):
        children (Union[Unset, List['AccountBookBalance']]):
    """

    id: str
    balance: Union[Unset, str] = 0
    increse: Union[Unset, str] = 0
    decrese: Union[Unset, str] = 0
    net_balance: Union[Unset, str] = 0
    net_increse: Union[Unset, str] = 0
    net_decrese: Union[Unset, str] = 0
    children: Union[Unset, List["AccountBookBalance"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        balance = self.balance
        increse = self.increse
        decrese = self.decrese
        net_balance = self.net_balance
        net_increse = self.net_increse
        net_decrese = self.net_decrese
        children: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()

                children.append(children_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if balance is not UNSET:
            field_dict["balance"] = balance
        if increse is not UNSET:
            field_dict["increse"] = increse
        if decrese is not UNSET:
            field_dict["decrese"] = decrese
        if net_balance is not UNSET:
            field_dict["net_balance"] = net_balance
        if net_increse is not UNSET:
            field_dict["net_increse"] = net_increse
        if net_decrese is not UNSET:
            field_dict["net_decrese"] = net_decrese
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        balance = d.pop("balance", UNSET)

        increse = d.pop("increse", UNSET)

        decrese = d.pop("decrese", UNSET)

        net_balance = d.pop("net_balance", UNSET)

        net_increse = d.pop("net_increse", UNSET)

        net_decrese = d.pop("net_decrese", UNSET)

        children = []
        _children = d.pop("children", UNSET)
        for children_item_data in _children or []:
            children_item = AccountBookBalance.from_dict(children_item_data)

            children.append(children_item)

        account_book_balance = cls(
            id=id,
            balance=balance,
            increse=increse,
            decrese=decrese,
            net_balance=net_balance,
            net_increse=net_increse,
            net_decrese=net_decrese,
            children=children,
        )

        account_book_balance.additional_properties = d
        return account_book_balance

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
