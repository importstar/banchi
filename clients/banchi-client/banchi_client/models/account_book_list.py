from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.account_book import AccountBook


T = TypeVar("T", bound="AccountBookList")


@_attrs_define
class AccountBookList:
    """
    Attributes:
        account_books (list['AccountBook']):
    """

    account_books: list["AccountBook"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_books = []
        for account_books_item_data in self.account_books:
            account_books_item = account_books_item_data.to_dict()
            account_books.append(account_books_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_books": account_books,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.account_book import AccountBook

        d = dict(src_dict)
        account_books = []
        _account_books = d.pop("account_books")
        for account_books_item_data in _account_books:
            account_books_item = AccountBook.from_dict(account_books_item_data)

            account_books.append(account_books_item)

        account_book_list = cls(
            account_books=account_books,
        )

        account_book_list.additional_properties = d
        return account_book_list

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
