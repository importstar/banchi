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
        id (str):  Example: 0.
        account (ReferenceAccount):
        parent (Union['ReferenceAccountBook', None]):
        creator (ReferenceUser):
        display_name (str):
        description (Union[Unset, str]):  Default: ''. Example: Description.
        type (Union[Unset, AccountTypeEnum]):  Default: AccountTypeEnum.ASSET.
        smallest_fraction (Union[Unset, SmallestFractionEnum]):  Default: 100.
        currency (Union[Unset, CurrencyEnum]):  Default: CurrencyEnum.THB.
        status (Union[Unset, str]):  Default: 'active'. Example: active.
    """

    name: str
    id: str
    account: "ReferenceAccount"
    parent: Union["ReferenceAccountBook", None]
    creator: "ReferenceUser"
    display_name: str
    description: Union[Unset, str] = ""
    type: Union[Unset, AccountTypeEnum] = AccountTypeEnum.ASSET
    smallest_fraction: Union[Unset, SmallestFractionEnum] = 100
    currency: Union[Unset, CurrencyEnum] = CurrencyEnum.THB
    status: Union[Unset, str] = "active"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.reference_account_book import ReferenceAccountBook

        name = self.name
        id = self.id
        account = self.account.to_dict()

        parent: Union[Dict[str, Any], None]

        if isinstance(self.parent, ReferenceAccountBook):
            parent = self.parent.to_dict()

        else:
            parent = self.parent

        creator = self.creator.to_dict()

        display_name = self.display_name
        description = self.description
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        smallest_fraction: Union[Unset, int] = UNSET
        if not isinstance(self.smallest_fraction, Unset):
            smallest_fraction = self.smallest_fraction.value

        currency: Union[Unset, str] = UNSET
        if not isinstance(self.currency, Unset):
            currency = self.currency.value

        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "account": account,
                "parent": parent,
                "creator": creator,
                "display_name": display_name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type
        if smallest_fraction is not UNSET:
            field_dict["smallest_fraction"] = smallest_fraction
        if currency is not UNSET:
            field_dict["currency"] = currency
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

        display_name = d.pop("display_name")

        description = d.pop("description", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, AccountTypeEnum]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = AccountTypeEnum(_type)

        _smallest_fraction = d.pop("smallest_fraction", UNSET)
        smallest_fraction: Union[Unset, SmallestFractionEnum]
        if isinstance(_smallest_fraction, Unset):
            smallest_fraction = UNSET
        else:
            smallest_fraction = SmallestFractionEnum(_smallest_fraction)

        _currency = d.pop("currency", UNSET)
        currency: Union[Unset, CurrencyEnum]
        if isinstance(_currency, Unset):
            currency = UNSET
        else:
            currency = CurrencyEnum(_currency)

        status = d.pop("status", UNSET)

        account_book = cls(
            name=name,
            id=id,
            account=account,
            parent=parent,
            creator=creator,
            display_name=display_name,
            description=description,
            type=type,
            smallest_fraction=smallest_fraction,
            currency=currency,
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
