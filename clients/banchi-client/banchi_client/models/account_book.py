from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
        increase (str):
        decrease (str):
        balance (str):
        description (Union[Unset, str]):  Default: ''. Example: Description.
        type (Union[Unset, Any]):  Default: 'asset'. Example: asset.
        smallest_fraction (Union[Unset, Any]):  Default: 100. Example: 100.
        currency (Union[Unset, Any]):  Default: 'THB'. Example: THB.
        status (Union[Unset, str]):  Default: 'active'. Example: active.
    """

    name: str
    id: str
    account: "ReferenceAccount"
    parent: Union["ReferenceAccountBook", None]
    creator: "ReferenceUser"
    increase: str
    decrease: str
    balance: str
    description: Union[Unset, str] = ""
    type: Union[Unset, Any] = "asset"
    smallest_fraction: Union[Unset, Any] = 100
    currency: Union[Unset, Any] = "THB"
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

        increase = self.increase

        decrease = self.decrease

        balance = self.balance

        description = self.description

        type = self.type

        smallest_fraction = self.smallest_fraction

        currency = self.currency

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
                "increase": increase,
                "decrease": decrease,
                "balance": balance,
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

        increase = d.pop("increase")

        decrease = d.pop("decrease")

        balance = d.pop("balance")

        description = d.pop("description", UNSET)

        type = d.pop("type", UNSET)

        smallest_fraction = d.pop("smallest_fraction", UNSET)

        currency = d.pop("currency", UNSET)

        status = d.pop("status", UNSET)

        account_book = cls(
            name=name,
            id=id,
            account=account,
            parent=parent,
            creator=creator,
            increase=increase,
            decrease=decrease,
            balance=balance,
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
