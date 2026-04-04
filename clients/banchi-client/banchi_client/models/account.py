from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.currency_enum import CurrencyEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference_space import ReferenceSpace
    from ..models.reference_user import ReferenceUser


T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """
    Attributes:
        name (str):  Example: Account Name.
        description (str):  Example: Description.
        currency (CurrencyEnum):
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        space (ReferenceSpace):
        creator (ReferenceUser):
        status (str | Unset):  Default: 'active'. Example: active.
    """

    name: str
    description: str
    currency: CurrencyEnum
    id: str
    space: ReferenceSpace
    creator: ReferenceUser
    status: str | Unset = "active"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        currency = self.currency.value

        id = self.id

        space = self.space.to_dict()

        creator = self.creator.to_dict()

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "currency": currency,
                "id": id,
                "space": space,
                "creator": creator,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reference_space import ReferenceSpace
        from ..models.reference_user import ReferenceUser

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        currency = CurrencyEnum(d.pop("currency"))

        id = d.pop("id")

        space = ReferenceSpace.from_dict(d.pop("space"))

        creator = ReferenceUser.from_dict(d.pop("creator"))

        status = d.pop("status", UNSET)

        account = cls(
            name=name,
            description=description,
            currency=currency,
            id=id,
            space=space,
            creator=creator,
            status=status,
        )

        account.additional_properties = d
        return account

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
