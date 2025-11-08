from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AccountBookSummary")


@_attrs_define
class AccountBookSummary:
    """
    Attributes:
        id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        year (int):
        month (int):
        date (datetime.datetime):
        created_date (datetime.datetime):
        updated_date (datetime.datetime):
        increase (str | Unset):  Default: '0'.
        decrease (str | Unset):  Default: '0'.
        balance (str | Unset):  Default: '0'.
    """

    id: str
    year: int
    month: int
    date: datetime.datetime
    created_date: datetime.datetime
    updated_date: datetime.datetime
    increase: str | Unset = "0"
    decrease: str | Unset = "0"
    balance: str | Unset = "0"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        year = self.year

        month = self.month

        date = self.date.isoformat()

        created_date = self.created_date.isoformat()

        updated_date = self.updated_date.isoformat()

        increase = self.increase

        decrease = self.decrease

        balance = self.balance

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "year": year,
                "month": month,
                "date": date,
                "created_date": created_date,
                "updated_date": updated_date,
            }
        )
        if increase is not UNSET:
            field_dict["increase"] = increase
        if decrease is not UNSET:
            field_dict["decrease"] = decrease
        if balance is not UNSET:
            field_dict["balance"] = balance

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        year = d.pop("year")

        month = d.pop("month")

        date = isoparse(d.pop("date"))

        created_date = isoparse(d.pop("created_date"))

        updated_date = isoparse(d.pop("updated_date"))

        increase = d.pop("increase", UNSET)

        decrease = d.pop("decrease", UNSET)

        balance = d.pop("balance", UNSET)

        account_book_summary = cls(
            id=id,
            year=year,
            month=month,
            date=date,
            created_date=created_date,
            updated_date=updated_date,
            increase=increase,
            decrease=decrease,
            balance=balance,
        )

        account_book_summary.additional_properties = d
        return account_book_summary

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
