import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.space_role_role import SpaceRoleRole
from ..models.space_role_status import SpaceRoleStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference_space import ReferenceSpace
    from ..models.reference_user import ReferenceUser


T = TypeVar("T", bound="SpaceRole")


@_attrs_define
class SpaceRole:
    """
    Attributes:
        role (SpaceRoleRole):
        id (str):  Example: 0.
        added_by (ReferenceUser):
        updated_by (ReferenceUser):
        member (ReferenceUser):
        space (ReferenceSpace):
        created_date (datetime.datetime):
        updated_date (datetime.datetime):
        status (Union[Unset, SpaceRoleStatus]):  Default: SpaceRoleStatus.ACTIVE.
    """

    role: SpaceRoleRole
    id: str
    added_by: "ReferenceUser"
    updated_by: "ReferenceUser"
    member: "ReferenceUser"
    space: "ReferenceSpace"
    created_date: datetime.datetime
    updated_date: datetime.datetime
    status: Union[Unset, SpaceRoleStatus] = SpaceRoleStatus.ACTIVE
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role.value

        id = self.id

        added_by = self.added_by.to_dict()

        updated_by = self.updated_by.to_dict()

        member = self.member.to_dict()

        space = self.space.to_dict()

        created_date = self.created_date.isoformat()

        updated_date = self.updated_date.isoformat()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "id": id,
                "added_by": added_by,
                "updated_by": updated_by,
                "member": member,
                "space": space,
                "created_date": created_date,
                "updated_date": updated_date,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.reference_space import ReferenceSpace
        from ..models.reference_user import ReferenceUser

        d = src_dict.copy()
        role = SpaceRoleRole(d.pop("role"))

        id = d.pop("id")

        added_by = ReferenceUser.from_dict(d.pop("added_by"))

        updated_by = ReferenceUser.from_dict(d.pop("updated_by"))

        member = ReferenceUser.from_dict(d.pop("member"))

        space = ReferenceSpace.from_dict(d.pop("space"))

        created_date = isoparse(d.pop("created_date"))

        updated_date = isoparse(d.pop("updated_date"))

        _status = d.pop("status", UNSET)
        status: Union[Unset, SpaceRoleStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SpaceRoleStatus(_status)

        space_role = cls(
            role=role,
            id=id,
            added_by=added_by,
            updated_by=updated_by,
            member=member,
            space=space,
            created_date=created_date,
            updated_date=updated_date,
            status=status,
        )

        space_role.additional_properties = d
        return space_role

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
