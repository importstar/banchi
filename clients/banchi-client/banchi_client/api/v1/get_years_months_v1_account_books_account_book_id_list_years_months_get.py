from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_get_years_months_v1_account_books_account_book_id_list_years_months_get import (
    ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet,
)
from ...types import Response


def _get_kwargs(
    account_book_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/account-books/{account_book_id}/list-years-months",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet | None:
    if response.status_code == 200:
        response_200 = ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_book_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet]:
    """Get Years Months

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet]
    """

    kwargs = _get_kwargs(
        account_book_id=account_book_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_book_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet | None:
    """Get Years Months

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet
    """

    return sync_detailed(
        account_book_id=account_book_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    account_book_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet]:
    """Get Years Months

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet]
    """

    kwargs = _get_kwargs(
        account_book_id=account_book_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_book_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet | None:
    """Get Years Months

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseGetYearsMonthsV1AccountBooksAccountBookIdListYearsMonthsGet
    """

    return (
        await asyncio_detailed(
            account_book_id=account_book_id,
            client=client,
        )
    ).parsed
