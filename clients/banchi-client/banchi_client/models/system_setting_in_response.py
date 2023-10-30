from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast, List
from typing import cast, Union


T = TypeVar("T", bound="SystemSettingInResponse")


@_attrs_define
class SystemSettingInResponse:
    """
    Attributes:
        title_names (List[str]):
        banks (List[str]):
        bill_expired (Union[None, int]):
        year (Union[None, str]):
        vat (Union[None, float]):
    """

    title_names: List[str]
    banks: List[str]
    bill_expired: Union[None, int]
    year: Union[None, str]
    vat: Union[None, float]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title_names = self.title_names

        banks = self.banks

        bill_expired: Union[None, int]

        bill_expired = self.bill_expired

        year: Union[None, str]

        year = self.year

        vat: Union[None, float]

        vat = self.vat

        field_dict: Dict[str, Any] = {}
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title_names = cast(List[str], d.pop("title_names"))

        banks = cast(List[str], d.pop("banks"))

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

        system_setting_in_response = cls(
            title_names=title_names,
            banks=banks,
            bill_expired=bill_expired,
            year=year,
            vat=vat,
        )

        system_setting_in_response.additional_properties = d
        return system_setting_in_response

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
