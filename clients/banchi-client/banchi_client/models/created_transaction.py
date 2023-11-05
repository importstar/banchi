from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.currency_enum import CurrencyEnum

T = TypeVar("T", bound="CreatedTransaction")


@_attrs_define
class CreatedTransaction:
    """
    Attributes:
        description (str):  Example: Desctription.
        value (float):
        currency (CurrencyEnum):
        from_account_book_id (str):  Example: 0.
        to_account_book_id (str):  Example: 0.
    """

    description: str
    value: float
    currency: CurrencyEnum
    from_account_book_id: str
    to_account_book_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        value = self.value
        currency = self.currency.value

        from_account_book_id = self.from_account_book_id
        to_account_book_id = self.to_account_book_id

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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description")

        value = d.pop("value")

        currency = CurrencyEnum(d.pop("currency"))

        from_account_book_id = d.pop("from_account_book_id")

        to_account_book_id = d.pop("to_account_book_id")

        created_transaction = cls(
            description=description,
            value=value,
            currency=currency,
            from_account_book_id=from_account_book_id,
            to_account_book_id=to_account_book_id,
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
