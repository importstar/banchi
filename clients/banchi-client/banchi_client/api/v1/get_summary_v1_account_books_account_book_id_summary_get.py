from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_book_summary import AccountBookSummary
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    account_book_id: str,
    *,
    year: int,
    month: int,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["year"] = year

    params["month"] = month

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/account-books/{account_book_id}/summary",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AccountBookSummary, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = AccountBookSummary.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AccountBookSummary, HTTPValidationError]]:
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
    year: int,
    month: int,
) -> Response[Union[AccountBookSummary, HTTPValidationError]]:
    """Get Summary

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        year (int):
        month (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountBookSummary, HTTPValidationError]]
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
    *,
    client: AuthenticatedClient,
    year: int,
    month: int,
) -> Optional[Union[AccountBookSummary, HTTPValidationError]]:
    """Get Summary

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        year (int):
        month (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountBookSummary, HTTPValidationError]
    """

    return sync_detailed(
        account_book_id=account_book_id,
        client=client,
        year=year,
        month=month,
    ).parsed


async def asyncio_detailed(
    account_book_id: str,
    *,
    client: AuthenticatedClient,
    year: int,
    month: int,
) -> Response[Union[AccountBookSummary, HTTPValidationError]]:
    """Get Summary

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        year (int):
        month (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountBookSummary, HTTPValidationError]]
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
    *,
    client: AuthenticatedClient,
    year: int,
    month: int,
) -> Optional[Union[AccountBookSummary, HTTPValidationError]]:
    """Get Summary

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        year (int):
        month (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountBookSummary, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            account_book_id=account_book_id,
            client=client,
            year=year,
            month=month,
        )
    ).parsed
