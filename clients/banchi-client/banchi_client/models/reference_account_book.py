from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ReferenceAccountBook")


@_attrs_define
class ReferenceAccountBook:
    """
    Attributes:
        id (str):  Example: 0.
        name (str):  Example: Account Book Name.
        parent (Union['ReferenceAccountBook', None]):
        display_name (str):
    """

    id: str
    name: str
    parent: Union["ReferenceAccountBook", None]
    display_name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        parent: Union[Dict[str, Any], None]

        if isinstance(self.parent, ReferenceAccountBook):
            parent = self.parent.to_dict()

        else:
            parent = self.parent

        display_name = self.display_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "parent": parent,
                "display_name": display_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        def _parse_parent(data: object) -> Union["ReferenceAccountBook", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_type_0 = ReferenceAccountBook.from_dict(data)

                return parent_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ReferenceAccountBook", None], data)

        parent = _parse_parent(d.pop("parent"))

        display_name = d.pop("display_name")

        reference_account_book = cls(
            id=id,
            name=name,
            parent=parent,
            display_name=display_name,
        )

        reference_account_book.additional_properties = d
        return reference_account_book

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
