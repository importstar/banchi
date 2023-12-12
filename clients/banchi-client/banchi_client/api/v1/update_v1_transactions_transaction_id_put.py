from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.transaction import Transaction
from ...models.updated_transaction import UpdatedTransaction
from ...types import Response


def _get_kwargs(
    transaction_id: str,
    *,
    json_body: UpdatedTransaction,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v1/transactions/{transaction_id}".format(
            transaction_id=transaction_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Transaction]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Transaction.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, Transaction]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    transaction_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdatedTransaction,
) -> Response[Union[HTTPValidationError, Transaction]]:
    """Update

    Args:
        transaction_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        json_body (UpdatedTransaction):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Transaction]]
    """

    kwargs = _get_kwargs(
        transaction_id=transaction_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    transaction_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdatedTransaction,
) -> Optional[Union[HTTPValidationError, Transaction]]:
    """Update

    Args:
        transaction_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        json_body (UpdatedTransaction):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Transaction]
    """

    return sync_detailed(
        transaction_id=transaction_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    transaction_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdatedTransaction,
) -> Response[Union[HTTPValidationError, Transaction]]:
    """Update

    Args:
        transaction_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        json_body (UpdatedTransaction):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Transaction]]
    """

    kwargs = _get_kwargs(
        transaction_id=transaction_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    transaction_id: str,
    *,
    client: AuthenticatedClient,
    json_body: UpdatedTransaction,
) -> Optional[Union[HTTPValidationError, Transaction]]:
    """Update

    Args:
        transaction_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        json_body (UpdatedTransaction):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Transaction]
    """

    return (
        await asyncio_detailed(
            transaction_id=transaction_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
