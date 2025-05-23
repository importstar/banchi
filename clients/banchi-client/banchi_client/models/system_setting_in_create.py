from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SystemSettingInCreate")


@_attrs_define
class SystemSettingInCreate:
    """
    Attributes:
        title_names (list[str]):
        banks (list[str]):
        bill_expired (Union[None, int]):
        year (Union[None, str]):
        vat (Union[None, float]):
    """

    title_names: list[str]
    banks: list[str]
    bill_expired: Union[None, int]
    year: Union[None, str]
    vat: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title_names = self.title_names

        banks = self.banks

        bill_expired: Union[None, int]
        bill_expired = self.bill_expired

        year: Union[None, str]
        year = self.year

        vat: Union[None, float]
        vat = self.vat

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title_names": title_names,
                "banks": banks,
                "bill_expired": bill_expired,
                "year": year,
                "vat": vat,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title_names = cast(list[str], d.pop("title_names"))

        banks = cast(list[str], d.pop("banks"))

        def _parse_bill_expired(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        bill_expired = _parse_bill_expired(d.pop("bill_expired"))

        def _parse_year(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        year = _parse_year(d.pop("year"))

        def _parse_vat(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        vat = _parse_vat(d.pop("vat"))

        system_setting_in_create = cls(
            title_names=title_names,
            banks=banks,
            bill_expired=bill_expired,
            year=year,
            vat=vat,
        )

        system_setting_in_create.additional_properties = d
        return system_setting_in_create

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
