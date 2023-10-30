from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
        currency (str):
        spaces (List['Space']):
        creator (List['User']):
        field_id (Union[Unset, str]):  Example: 0.
    """

    name: str
    description: str
    currency: str
    spaces: List["Space"]
    creator: List["User"]
    field_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        currency = self.currency
        spaces = []
        for spaces_item_data in self.spaces:
            spaces_item = spaces_item_data.to_dict()

            spaces.append(spaces_item)

        creator = []
        for creator_item_data in self.creator:
            creator_item = creator_item_data.to_dict()

            creator.append(creator_item)

        field_id = self.field_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "currency": currency,
                "spaces": spaces,
                "creator": creator,
            }
        )
        if field_id is not UNSET:
            field_dict["_id"] = field_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.space import Space
        from ..models.user import User

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        currency = d.pop("currency")

        spaces = []
        _spaces = d.pop("spaces")
        for spaces_item_data in _spaces:
            spaces_item = Space.from_dict(spaces_item_data)

            spaces.append(spaces_item)

        creator = []
        _creator = d.pop("creator")
        for creator_item_data in _creator:
            creator_item = User.from_dict(creator_item_data)

            creator.append(creator_item)

        field_id = d.pop("_id", UNSET)

        account = cls(
            name=name,
            description=description,
            currency=currency,
            spaces=spaces,
            creator=creator,
            field_id=field_id,
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
