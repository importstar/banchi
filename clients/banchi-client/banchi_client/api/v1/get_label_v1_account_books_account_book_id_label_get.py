from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_book_label import AccountBookLabel
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    account_book_id: str,
) -> Dict[str, Any]:
    return {
        "method": "get",
        "url": "/v1/account-books/{account_book_id}/label".format(
            account_book_id=account_book_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AccountBookLabel, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AccountBookLabel.from_dict(response.json())

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
) -> Response[Union[AccountBookLabel, HTTPValidationError]]:
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
) -> Response[Union[AccountBookLabel, HTTPValidationError]]:
    """Get Label

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountBookLabel, HTTPValidationError]]
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
) -> Optional[Union[AccountBookLabel, HTTPValidationError]]:
    """Get Label

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountBookLabel, HTTPValidationError]
    """

    return sync_detailed(
        account_book_id=account_book_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    account_book_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AccountBookLabel, HTTPValidationError]]:
    """Get Label

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountBookLabel, HTTPValidationError]]
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
) -> Optional[Union[AccountBookLabel, HTTPValidationError]]:
    """Get Label

    Args:
        account_book_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountBookLabel, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            account_book_id=account_book_id,
            client=client,
        )
    ).parsed
