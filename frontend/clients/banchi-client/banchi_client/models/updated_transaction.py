import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.currency_enum import CurrencyEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdatedTransaction")


@_attrs_define
class UpdatedTransaction:
    """
    Attributes:
        description (str):  Example: Desctription.
        value (Union[float, str]):
        currency (CurrencyEnum):
        from_account_book_id (str):  Example: 0.
        to_account_book_id (str):  Example: 0.
        date (Union[Unset, datetime.datetime]):  Default: isoparse('2023-12-09T23:56:55.997848').
    """

    description: str
    value: Union[float, str]
    currency: CurrencyEnum
    from_account_book_id: str
    to_account_book_id: str
    date: Union[Unset, datetime.datetime] = isoparse("2023-12-09T23:56:55.997848")
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

        updated_transaction = cls(
            description=description,
            value=value,
            currency=currency,
            from_account_book_id=from_account_book_id,
            to_account_book_id=to_account_book_id,
            date=date,
        )

        updated_transaction.additional_properties = d
        return updated_transaction

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
