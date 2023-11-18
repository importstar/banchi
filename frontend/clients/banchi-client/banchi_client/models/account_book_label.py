from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountBookLabel")


@_attrs_define
class AccountBookLabel:
    """
    Attributes:
        positive (Union[Unset, str]):  Default: 'increase'. Example: increase.
        negative (Union[Unset, str]):  Default: 'decrease'. Example: decrease.
    """

    positive: Union[Unset, str] = "increase"
    negative: Union[Unset, str] = "decrease"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        positive = self.positive
        negative = self.negative

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if positive is not UNSET:
            field_dict["positive"] = positive
        if negative is not UNSET:
            field_dict["negative"] = negative

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        positive = d.pop("positive", UNSET)

        negative = d.pop("negative", UNSET)

        account_book_label = cls(
            positive=positive,
            negative=negative,
        )

        account_book_label.additional_properties = d
        return account_book_label

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
