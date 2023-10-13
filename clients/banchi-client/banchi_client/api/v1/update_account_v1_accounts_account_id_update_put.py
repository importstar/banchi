from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account import Account
from ...models.created_account import CreatedAccount
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    account_id: str,
    *,
    json_body: CreatedAccount,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v1/accounts/{account_id}/update".format(
            account_id=account_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Account, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Account.from_dict(response.json())

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
) -> Response[Union[Account, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    account_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedAccount,
) -> Response[Union[Account, HTTPValidationError]]:
    """Update Account

    Args:
        account_id (str):
        json_body (CreatedAccount):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Account, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    account_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedAccount,
) -> Optional[Union[Account, HTTPValidationError]]:
    """Update Account

    Args:
        account_id (str):
        json_body (CreatedAccount):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Account, HTTPValidationError]
    """

    return sync_detailed(
        account_id=account_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    account_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedAccount,
) -> Response[Union[Account, HTTPValidationError]]:
    """Update Account

    Args:
        account_id (str):
        json_body (CreatedAccount):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Account, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    account_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedAccount,
) -> Optional[Union[Account, HTTPValidationError]]:
    """Update Account

    Args:
        account_id (str):
        json_body (CreatedAccount):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Account, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            account_id=account_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
