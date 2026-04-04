from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.transaction_list import TransactionList
from ...types import UNSET, Response


def _get_kwargs(
    *,
    from_account_book_id: None | str,
    to_account_book_id: None | str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_from_account_book_id: None | str
    json_from_account_book_id = from_account_book_id
    params["from_account_book_id"] = json_from_account_book_id

    json_to_account_book_id: None | str
    json_to_account_book_id = to_account_book_id
    params["to_account_book_id"] = json_to_account_book_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/transactions/get_recursive",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TransactionList | None:
    if response.status_code == 200:
        response_200 = TransactionList.from_dict(response.json())

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
) -> Response[HTTPValidationError | TransactionList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    from_account_book_id: None | str,
    to_account_book_id: None | str,
) -> Response[HTTPValidationError | TransactionList]:
    """Get Recursive

    Args:
        from_account_book_id (None | str):
        to_account_book_id (None | str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TransactionList]
    """

    kwargs = _get_kwargs(
        from_account_book_id=from_account_book_id,
        to_account_book_id=to_account_book_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    from_account_book_id: None | str,
    to_account_book_id: None | str,
) -> HTTPValidationError | TransactionList | None:
    """Get Recursive

    Args:
        from_account_book_id (None | str):
        to_account_book_id (None | str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TransactionList
    """

    return sync_detailed(
        client=client,
        from_account_book_id=from_account_book_id,
        to_account_book_id=to_account_book_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    from_account_book_id: None | str,
    to_account_book_id: None | str,
) -> Response[HTTPValidationError | TransactionList]:
    """Get Recursive

    Args:
        from_account_book_id (None | str):
        to_account_book_id (None | str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TransactionList]
    """

    kwargs = _get_kwargs(
        from_account_book_id=from_account_book_id,
        to_account_book_id=to_account_book_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    from_account_book_id: None | str,
    to_account_book_id: None | str,
) -> HTTPValidationError | TransactionList | None:
    """Get Recursive

    Args:
        from_account_book_id (None | str):
        to_account_book_id (None | str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TransactionList
    """

    return (
        await asyncio_detailed(
            client=client,
            from_account_book_id=from_account_book_id,
            to_account_book_id=to_account_book_id,
        )
    ).parsed
