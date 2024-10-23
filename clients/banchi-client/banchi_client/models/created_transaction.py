import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.currency_enum import CurrencyEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreatedTransaction")


@_attrs_define
class CreatedTransaction:
    """
    Attributes:
        description (str):  Example: Desctription.
        value (Union[float, str]):
        currency (CurrencyEnum):
        from_account_book_id (str):  Example: 0.
        to_account_book_id (str):  Example: 0.
        date (Union[Unset, datetime.datetime]):  Default: isoparse('2024-10-23T11:24:03.219397').
        tags (Union[Unset, List[str]]):
        remarks (Union[None, Unset, str]):  Default: ''. Example: Text Remark.
    """

    description: str
    value: Union[float, str]
    currency: CurrencyEnum
    from_account_book_id: str
    to_account_book_id: str
    date: Union[Unset, datetime.datetime] = isoparse("2024-10-23T11:24:03.219397")
    tags: Union[Unset, List[str]] = UNSET
    remarks: Union[None, Unset, str] = ""
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        value: Union[float, str]
        value = self.value

        currency = self.currency.value

        from_account_book_id = self.from_account_book_id

        to_account_book_id = self.to_account_book_id

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        remarks: Union[None, Unset, str]
        if isinstance(self.remarks, Unset):
            remarks = UNSET
        else:
            remarks = self.remarks

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "value": value,
                "currency": currency,
                "from_account_book_id": from_account_book_id,
                "to_account_book_id": to_account_book_id,
            }
        )
        if date is not UNSET:
            field_dict["date"] = date
        if tags is not UNSET:
            field_dict["tags"] = tags
        if remarks is not UNSET:
            field_dict["remarks"] = remarks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description")

        def _parse_value(data: object) -> Union[float, str]:
            return cast(Union[float, str], data)

        value = _parse_value(d.pop("value"))

        currency = CurrencyEnum(d.pop("currency"))

        from_account_book_id = d.pop("from_account_book_id")

        to_account_book_id = d.pop("to_account_book_id")

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        tags = cast(List[str], d.pop("tags", UNSET))

        def _parse_remarks(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        remarks = _parse_remarks(d.pop("remarks", UNSET))

        created_transaction = cls(
            description=description,
            value=value,
            currency=currency,
            from_account_book_id=from_account_book_id,
            to_account_book_id=to_account_book_id,
            date=date,
            tags=tags,
            remarks=remarks,
        )

        created_transaction.additional_properties = d
        return created_transaction

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
