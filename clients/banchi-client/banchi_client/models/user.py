from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from dateutil.parser import isoparse
from typing import cast, Union
import datetime
from ..types import UNSET, Unset
from typing import Union


T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        email (str):  Example: admin@email.local.
        username (str):  Example: admin.
        first_name (str):  Example: Firstname.
        last_name (str):  Example: Lastname.
        field_id (Union[Unset, str]):  Example: 0.
        last_login_date (Union[None, Unset, datetime.datetime]):  Example: 2023-01-01T00:00:00.000000.
    """

    email: str
    username: str
    first_name: str
    last_name: str
    field_id: Union[Unset, str] = UNSET
    last_login_date: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        username = self.username
        first_name = self.first_name
        last_name = self.last_name
        field_id = self.field_id
        last_login_date: Union[None, Unset, str]
        if isinstance(self.last_login_date, Unset):
            last_login_date = UNSET

        elif isinstance(self.last_login_date, datetime.datetime):
            last_login_date = UNSET
            if not isinstance(self.last_login_date, Unset):
                last_login_date = self.last_login_date.isoformat()

        else:
            last_login_date = self.last_login_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        )
        if field_id is not UNSET:
            field_dict["_id"] = field_id
        if last_login_date is not UNSET:
            field_dict["last_login_date"] = last_login_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        username = d.pop("username")

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        field_id = d.pop("_id", UNSET)

        def _parse_last_login_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                _last_login_date_type_0 = data
                last_login_date_type_0: Union[Unset, datetime.datetime]
                if isinstance(_last_login_date_type_0, Unset):
                    last_login_date_type_0 = UNSET
                else:
                    last_login_date_type_0 = isoparse(_last_login_date_type_0)

                return last_login_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_login_date = _parse_last_login_date(d.pop("last_login_date", UNSET))

        user = cls(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            field_id=field_id,
            last_login_date=last_login_date,
        )

        user.additional_properties = d
        return user

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
