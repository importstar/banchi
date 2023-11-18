from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AccountBookBalance")


@_attrs_define
class AccountBookBalance:
    """
    Attributes:
        balance (str):
        increse (str):
        decrese (str):
    """

    balance: str
    increse: str
    decrese: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        balance = self.balance
        increse = self.increse
        decrese = self.decrese

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "balance": balance,
                "increse": increse,
                "decrese": decrese,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        balance = d.pop("balance")

        increse = d.pop("increse")

        decrese = d.pop("decrese")

        account_book_balance = cls(
            balance=balance,
            increse=increse,
            decrese=decrese,
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
