from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_type_enum import AccountTypeEnum
from ..models.currency_enum import CurrencyEnum
from ..models.smallest_fraction_enum import SmallestFractionEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.account import Account
    from ..models.user import User


T = TypeVar("T", bound="AccountBook")


@_attrs_define
class AccountBook:
    """
    Attributes:
        name (str):  Example: Account Name.
        description (str):  Example: Description.
        type (AccountTypeEnum):
        smallest_fraction (SmallestFractionEnum):
        currency (CurrencyEnum):
        account (Account):
        creator (User):
        field_id (Union[Unset, str]):  Example: 0.
        status (Union[Unset, str]):  Default: 'active'. Example: active.
    """

    name: str
    description: str
    type: AccountTypeEnum
    smallest_fraction: SmallestFractionEnum
    currency: CurrencyEnum
    account: "Account"
    creator: "User"
    field_id: Union[Unset, str] = UNSET
    status: Union[Unset, str] = "active"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        type = self.type.value

        smallest_fraction = self.smallest_fraction.value

        currency = self.currency.value

        account = self.account.to_dict()

        creator = self.creator.to_dict()

        field_id = self.field_id
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
                "account": account,
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
        from ..models.account import Account
        from ..models.user import User

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        type = AccountTypeEnum(d.pop("type"))

        smallest_fraction = SmallestFractionEnum(d.pop("smallest_fraction"))

        currency = CurrencyEnum(d.pop("currency"))

        account = Account.from_dict(d.pop("account"))

        creator = User.from_dict(d.pop("creator"))

        field_id = d.pop("_id", UNSET)

        status = d.pop("status", UNSET)

        account_book = cls(
            name=name,
            description=description,
            type=type,
            smallest_fraction=smallest_fraction,
            currency=currency,
            account=account,
            creator=creator,
            field_id=field_id,
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
