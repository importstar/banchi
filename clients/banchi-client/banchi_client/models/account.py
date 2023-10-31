from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.currency_enum import CurrencyEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.space import Space
    from ..models.user import User


T = TypeVar("T", bound="Account")


@_attrs_define
class Account:
    """
    Attributes:
        name (str):  Example: Account Name.
        description (str):  Example: Description.
        currency (CurrencyEnum):
        space (Space):
        creator (User):
        field_id (Union[Unset, str]):  Example: 0.
        status (Union[Unset, str]):  Default: 'active'. Example: active.
    """

    name: str
    description: str
    currency: CurrencyEnum
    space: "Space"
    creator: "User"
    field_id: Union[Unset, str] = UNSET
    status: Union[Unset, str] = "active"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        currency = self.currency.value

        space = self.space.to_dict()

        creator = self.creator.to_dict()

        field_id = self.field_id
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "currency": currency,
                "space": space,
                "creator": creator,
            }
        )
        if field_id is not UNSET:
            field_dict["_id"] = field_id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.space import Space
        from ..models.user import User

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        currency = CurrencyEnum(d.pop("currency"))

        space = Space.from_dict(d.pop("space"))

        creator = User.from_dict(d.pop("creator"))

        field_id = d.pop("_id", UNSET)

        status = d.pop("status", UNSET)

        account = cls(
            name=name,
            description=description,
            currency=currency,
            space=space,
            creator=creator,
            field_id=field_id,
            status=status,
        )

        account.additional_properties = d
        return account

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
