from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_book import AccountBook
from ...models.http_validation_error import HTTPValidationError
from ...models.updated_account_book import UpdatedAccountBook
from ...types import Response


def _get_kwargs(
    account_book_id: str,
    *,
    body: UpdatedAccountBook,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/v1/account-books/{account_book_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AccountBook, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AccountBook.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AccountBook, HTTPValidationError]]:
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
    body: UpdatedAccountBook,
) -> Response[Union[AccountBook, HTTPValidationError]]:
    """Update

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (UpdatedAccountBook):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountBook, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        account_book_id=account_book_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_book_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdatedAccountBook,
) -> Optional[Union[AccountBook, HTTPValidationError]]:
    """Update

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (UpdatedAccountBook):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountBook, HTTPValidationError]
    """

    return sync_detailed(
        account_book_id=account_book_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    account_book_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdatedAccountBook,
) -> Response[Union[AccountBook, HTTPValidationError]]:
    """Update

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (UpdatedAccountBook):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountBook, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        account_book_id=account_book_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_book_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdatedAccountBook,
) -> Optional[Union[AccountBook, HTTPValidationError]]:
    """Update

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (UpdatedAccountBook):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountBook, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            account_book_id=account_book_id,
            client=client,
            body=body,
        )
    ).parsed
