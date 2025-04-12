from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_book_list import AccountBookList
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    account_book_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/account-books/{account_book_id}/children",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AccountBookList, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = AccountBookList.from_dict(response.json())

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
) -> Response[Union[AccountBookList, HTTPValidationError]]:
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
) -> Response[Union[AccountBookList, HTTPValidationError]]:
    """Get Children

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountBookList, HTTPValidationError]]
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
) -> Optional[Union[AccountBookList, HTTPValidationError]]:
    """Get Children

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountBookList, HTTPValidationError]
    """

    return sync_detailed(
        account_book_id=account_book_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    account_book_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AccountBookList, HTTPValidationError]]:
    """Get Children

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountBookList, HTTPValidationError]]
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
) -> Optional[Union[AccountBookList, HTTPValidationError]]:
    """Get Children

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountBookList, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            account_book_id=account_book_id,
            client=client,
        )
    ).parsed
