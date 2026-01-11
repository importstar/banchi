from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_get_balance_by_year_month_v1_account_books_account_book_id_balance_year_month_get import (
    ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet,
)
from ...types import Response


def _get_kwargs(
    account_book_id: str,
    year: int,
    month: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/account-books/{account_book_id}/balance/{year}/{month}".format(
            account_book_id=quote(str(account_book_id), safe=""),
            year=quote(str(year), safe=""),
            month=quote(str(month), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    HTTPValidationError
    | ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet
    | None
):
    if response.status_code == 200:
        response_200 = ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet.from_dict(
            response.json()
        )

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    HTTPValidationError
    | ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_book_id: str,
    year: int,
    month: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    HTTPValidationError
    | ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet
]:
    """Get Balance By Year Month

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        year (int):
        month (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet]
    """

    kwargs = _get_kwargs(
        account_book_id=account_book_id,
        year=year,
        month=month,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_book_id: str,
    year: int,
    month: int,
    *,
    client: AuthenticatedClient,
) -> (
    HTTPValidationError
    | ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet
    | None
):
    """Get Balance By Year Month

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        year (int):
        month (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet
    """

    return sync_detailed(
        account_book_id=account_book_id,
        year=year,
        month=month,
        client=client,
    ).parsed


async def asyncio_detailed(
    account_book_id: str,
    year: int,
    month: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    HTTPValidationError
    | ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet
]:
    """Get Balance By Year Month

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        year (int):
        month (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet]
    """

    kwargs = _get_kwargs(
        account_book_id=account_book_id,
        year=year,
        month=month,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_book_id: str,
    year: int,
    month: int,
    *,
    client: AuthenticatedClient,
) -> (
    HTTPValidationError
    | ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet
    | None
):
    """Get Balance By Year Month

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        year (int):
        month (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseGetBalanceByYearMonthV1AccountBooksAccountBookIdBalanceYearMonthGet
    """

    return (
        await asyncio_detailed(
            account_book_id=account_book_id,
            year=year,
            month=month,
            client=client,
        )
    ).parsed
