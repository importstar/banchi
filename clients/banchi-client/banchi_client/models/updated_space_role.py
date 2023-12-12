from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.updated_space_role_role import UpdatedSpaceRoleRole

T = TypeVar("T", bound="UpdatedSpaceRole")


@_attrs_define
class UpdatedSpaceRole:
    """
    Attributes:
        role (UpdatedSpaceRoleRole):
        member_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
    """

    role: UpdatedSpaceRoleRole
    member_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role.value

        member_id = self.member_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "member_id": member_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role = UpdatedSpaceRoleRole(d.pop("role"))

        member_id = d.pop("member_id")

        updated_space_role = cls(
            role=role,
            member_id=member_id,
        )

        updated_space_role.additional_properties = d
        return updated_space_role

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
