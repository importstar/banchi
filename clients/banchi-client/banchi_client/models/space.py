from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference_user import ReferenceUser


T = TypeVar("T", bound="Space")


@_attrs_define
class Space:
    """
    Attributes:
        name (str):  Example: Space Name.
        code (None | str):  Example: Space Code.
        tax_id (None | str):  Example: Text ID.
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        owner (ReferenceUser):
        status (str | Unset):  Default: 'active'. Example: active.
    """

    name: str
    code: None | str
    tax_id: None | str
    id: str
    owner: ReferenceUser
    status: str | Unset = "active"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        code: None | str
        code = self.code

        tax_id: None | str
        tax_id = self.tax_id

        id = self.id

        owner = self.owner.to_dict()

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "code": code,
                "tax_id": tax_id,
                "id": id,
                "owner": owner,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reference_user import ReferenceUser

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        code = _parse_code(d.pop("code"))

        def _parse_tax_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        tax_id = _parse_tax_id(d.pop("tax_id"))

        id = d.pop("id")

        owner = ReferenceUser.from_dict(d.pop("owner"))

        status = d.pop("status", UNSET)

        space = cls(
            name=name,
            code=code,
            tax_id=tax_id,
            id=id,
            owner=owner,
            status=status,
        )

        space.additional_properties = d
        return space

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
