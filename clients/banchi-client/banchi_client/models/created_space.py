from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreatedSpace")


@_attrs_define
class CreatedSpace:
    """
    Attributes:
        name (str):  Example: Space Name.
        code (Union[None, str]):  Example: Space Code.
        tax_id (Union[None, str]):  Example: Text ID.
    """

    name: str
    code: Union[None, str]
    tax_id: Union[None, str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        code: Union[None, str]
        code = self.code

        tax_id: Union[None, str]
        tax_id = self.tax_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "code": code,
                "tax_id": tax_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        def _parse_code(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        code = _parse_code(d.pop("code"))

        def _parse_tax_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        tax_id = _parse_tax_id(d.pop("tax_id"))

        created_space = cls(
            name=name,
            code=code,
            tax_id=tax_id,
        )

        created_space.additional_properties = d
        return created_space

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
