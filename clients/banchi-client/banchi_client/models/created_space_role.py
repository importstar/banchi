from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.created_space_role_role import CreatedSpaceRoleRole

T = TypeVar("T", bound="CreatedSpaceRole")


@_attrs_define
class CreatedSpaceRole:
    """
    Attributes:
        role (CreatedSpaceRoleRole):
        member_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
    """

    role: CreatedSpaceRoleRole
    member_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role.value

        member_id = self.member_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "member_id": member_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = CreatedSpaceRoleRole(d.pop("role"))

        member_id = d.pop("member_id")

        created_space_role = cls(
            role=role,
            member_id=member_id,
        )

        created_space_role.additional_properties = d
        return created_space_role

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
