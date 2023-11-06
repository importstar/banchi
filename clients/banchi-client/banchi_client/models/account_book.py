from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_type_enum import AccountTypeEnum
from ..models.currency_enum import CurrencyEnum
from ..models.smallest_fraction_enum import SmallestFractionEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference_account import ReferenceAccount
    from ..models.reference_account_book import ReferenceAccountBook
    from ..models.reference_user import ReferenceUser


T = TypeVar("T", bound="AccountBook")


@_attrs_define
class AccountBook:
    """
    Attributes:
        name (str):  Example: Account Book Name.
        description (str):  Example: Description.
        type (AccountTypeEnum):
        smallest_fraction (SmallestFractionEnum):
        currency (CurrencyEnum):
        id (str):  Example: 0.
        account (ReferenceAccount):
        parent (Union['ReferenceAccountBook', None]):
        creator (ReferenceUser):
        status (Union[Unset, str]):  Default: 'active'. Example: active.
    """

    name: str
    description: str
    type: AccountTypeEnum
    smallest_fraction: SmallestFractionEnum
    currency: CurrencyEnum
    id: str
    account: "ReferenceAccount"
    parent: Union["ReferenceAccountBook", None]
    creator: "ReferenceUser"
    status: Union[Unset, str] = "active"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.reference_account_book import ReferenceAccountBook

        name = self.name
        description = self.description
        type = self.type.value

        smallest_fraction = self.smallest_fraction.value

        currency = self.currency.value

        id = self.id
        account = self.account.to_dict()

        parent: Union[Dict[str, Any], None]

        if isinstance(self.parent, ReferenceAccountBook):
            parent = self.parent.to_dict()

        else:
            parent = self.parent

        creator = self.creator.to_dict()

        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "type": type,
                "smallest_fraction": smallest_fraction,
                "currency": currency,
                "id": id,
                "account": account,
                "parent": parent,
                "creator": creator,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.reference_account import ReferenceAccount
        from ..models.reference_account_book import ReferenceAccountBook
        from ..models.reference_user import ReferenceUser

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        type = AccountTypeEnum(d.pop("type"))

        smallest_fraction = SmallestFractionEnum(d.pop("smallest_fraction"))

        currency = CurrencyEnum(d.pop("currency"))

        id = d.pop("id")

        account = ReferenceAccount.from_dict(d.pop("account"))

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

        creator = ReferenceUser.from_dict(d.pop("creator"))

        status = d.pop("status", UNSET)

        account_book = cls(
            name=name,
            description=description,
            type=type,
            smallest_fraction=smallest_fraction,
            currency=currency,
            id=id,
            account=account,
            parent=parent,
            creator=creator,
            status=status,
        )

        account_book.additional_properties = d
        return account_book

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
