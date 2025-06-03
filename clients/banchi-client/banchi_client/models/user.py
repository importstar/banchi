import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        email (str):  Example: admin@email.local.
        username (str):  Example: admin.
        first_name (str):  Example: Firstname.
        last_name (str):  Example: Lastname.
        id (str):  Example: 0.
        roles (Union[None, list[str]]):  Example: ['user'].
        last_login_date (Union[None, Unset, datetime.datetime]):  Example: 2023-01-01T00:00:00.000000.
        register_date (Union[None, Unset, datetime.datetime]):  Example: 2023-01-01T00:00:00.000000.
    """

    email: str
    username: str
    first_name: str
    last_name: str
    id: str
    roles: Union[None, list[str]]
    last_login_date: Union[None, Unset, datetime.datetime] = UNSET
    register_date: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        username = self.username

        first_name = self.first_name

        last_name = self.last_name

        id = self.id

        roles: Union[None, list[str]]
        if isinstance(self.roles, list):
            roles = self.roles

        else:
            roles = self.roles

        last_login_date: Union[None, Unset, str]
        if isinstance(self.last_login_date, Unset):
            last_login_date = UNSET
        elif isinstance(self.last_login_date, datetime.datetime):
            last_login_date = self.last_login_date.isoformat()
        else:
            last_login_date = self.last_login_date

        register_date: Union[None, Unset, str]
        if isinstance(self.register_date, Unset):
            register_date = UNSET
        elif isinstance(self.register_date, datetime.datetime):
            register_date = self.register_date.isoformat()
        else:
            register_date = self.register_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "id": id,
                "roles": roles,
            }
        )
        if last_login_date is not UNSET:
            field_dict["last_login_date"] = last_login_date
        if register_date is not UNSET:
            field_dict["register_date"] = register_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        username = d.pop("username")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        id = d.pop("id")

        def _parse_roles(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                roles_type_0 = cast(list[str], data)

                return roles_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        roles = _parse_roles(d.pop("roles"))

        def _parse_last_login_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_login_date_type_0 = isoparse(data)

                return last_login_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_login_date = _parse_last_login_date(d.pop("last_login_date", UNSET))

        def _parse_register_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                register_date_type_0 = isoparse(data)

                return register_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        register_date = _parse_register_date(d.pop("register_date", UNSET))

        user = cls(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            id=id,
            roles=roles,
            last_login_date=last_login_date,
            register_date=register_date,
        )

        user.additional_properties = d
        return user

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
