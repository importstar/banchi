from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RegisteredUser")


@_attrs_define
class RegisteredUser:
    """
    Attributes:
        email (str):  Example: admin@email.local.
        username (str):  Example: admin.
        first_name (str):  Example: Firstname.
        last_name (str):  Example: Lastname.
        password (str):  Example: password.
    """

    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        username = self.username
        first_name = self.first_name
        last_name = self.last_name
        password = self.password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        username = d.pop("username")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        password = d.pop("password")

        registered_user = cls(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        registered_user.additional_properties = d
        return registered_user

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
