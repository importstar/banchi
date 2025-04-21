import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.currency_enum import CurrencyEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reference_account_book import ReferenceAccountBook
    from ..models.reference_user import ReferenceUser


T = TypeVar("T", bound="Transaction")


@_attrs_define
class Transaction:
    """
    Attributes:
        description (str):  Example: Desctription.
        value (str):
        currency (CurrencyEnum):
        id (str):  Example: 0.
        from_account_book (ReferenceAccountBook):
        to_account_book (ReferenceAccountBook):
        creator (ReferenceUser):
        updated_by (ReferenceUser):
        date (Union[Unset, datetime.datetime]):  Default: isoparse('2025-04-21T21:31:39.617671').
        tags (Union[Unset, list[str]]):
        remarks (Union[None, Unset, str]):  Default: ''. Example: Text Remark.
        status (Union[Unset, str]):  Default: 'active'. Example: active.
    """

    description: str
    value: str
    currency: CurrencyEnum
    id: str
    from_account_book: "ReferenceAccountBook"
    to_account_book: "ReferenceAccountBook"
    creator: "ReferenceUser"
    updated_by: "ReferenceUser"
    date: Union[Unset, datetime.datetime] = isoparse("2025-04-21T21:31:39.617671")
    tags: Union[Unset, list[str]] = UNSET
    remarks: Union[None, Unset, str] = ""
    status: Union[Unset, str] = "active"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        value = self.value

        currency = self.currency.value

        id = self.id

        from_account_book = self.from_account_book.to_dict()

        to_account_book = self.to_account_book.to_dict()

        creator = self.creator.to_dict()

        updated_by = self.updated_by.to_dict()

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        remarks: Union[None, Unset, str]
        if isinstance(self.remarks, Unset):
            remarks = UNSET
        else:
            remarks = self.remarks

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "value": value,
                "currency": currency,
                "id": id,
                "from_account_book": from_account_book,
                "to_account_book": to_account_book,
                "creator": creator,
                "updated_by": updated_by,
            }
        )
        if date is not UNSET:
            field_dict["date"] = date
        if tags is not UNSET:
            field_dict["tags"] = tags
        if remarks is not UNSET:
            field_dict["remarks"] = remarks
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reference_account_book import ReferenceAccountBook
        from ..models.reference_user import ReferenceUser

        d = dict(src_dict)
        description = d.pop("description")

        value = d.pop("value")

        currency = CurrencyEnum(d.pop("currency"))

        id = d.pop("id")

        from_account_book = ReferenceAccountBook.from_dict(d.pop("from_account_book"))

        to_account_book = ReferenceAccountBook.from_dict(d.pop("to_account_book"))

        creator = ReferenceUser.from_dict(d.pop("creator"))

        updated_by = ReferenceUser.from_dict(d.pop("updated_by"))

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_remarks(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        remarks = _parse_remarks(d.pop("remarks", UNSET))

        status = d.pop("status", UNSET)

        transaction = cls(
            description=description,
            value=value,
            currency=currency,
            id=id,
            from_account_book=from_account_book,
            to_account_book=to_account_book,
            creator=creator,
            updated_by=updated_by,
            date=date,
            tags=tags,
            remarks=remarks,
            status=status,
        )

        transaction.additional_properties = d
        return transaction

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
