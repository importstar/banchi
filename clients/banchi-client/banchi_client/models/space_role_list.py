from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.space_role import SpaceRole


T = TypeVar("T", bound="SpaceRoleList")


@_attrs_define
class SpaceRoleList:
    """
    Attributes:
        space_roles (List['SpaceRole']):
    """

    space_roles: List["SpaceRole"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        space_roles = []
        for space_roles_item_data in self.space_roles:
            space_roles_item = space_roles_item_data.to_dict()

            space_roles.append(space_roles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "space_roles": space_roles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.space_role import SpaceRole

        d = src_dict.copy()
        space_roles = []
        _space_roles = d.pop("space_roles")
        for space_roles_item_data in _space_roles:
            space_roles_item = SpaceRole.from_dict(space_roles_item_data)

            space_roles.append(space_roles_item)

        space_role_list = cls(
            space_roles=space_roles,
        )

        space_role_list.additional_properties = d
        return space_role_list

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
