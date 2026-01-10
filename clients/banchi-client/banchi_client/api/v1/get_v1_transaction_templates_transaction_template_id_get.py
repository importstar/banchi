from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.transaction_template import TransactionTemplate
from ...types import Response


def _get_kwargs(
    transaction_template_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/transaction-templates/{transaction_template_id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TransactionTemplate | None:
    if response.status_code == 200:
        response_200 = TransactionTemplate.from_dict(response.json())

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
) -> Response[HTTPValidationError | TransactionTemplate]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    transaction_template_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | TransactionTemplate]:
    """Get

    Args:
        transaction_template_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TransactionTemplate]
    """

    kwargs = _get_kwargs(
        transaction_template_id=transaction_template_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    transaction_template_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | TransactionTemplate | None:
    """Get

    Args:
        transaction_template_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TransactionTemplate
    """

    return sync_detailed(
        transaction_template_id=transaction_template_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    transaction_template_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | TransactionTemplate]:
    """Get

    Args:
        transaction_template_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TransactionTemplate]
    """

    kwargs = _get_kwargs(
        transaction_template_id=transaction_template_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    transaction_template_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | TransactionTemplate | None:
    """Get

    Args:
        transaction_template_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TransactionTemplate
    """

    return (
        await asyncio_detailed(
            transaction_template_id=transaction_template_id,
            client=client,
        )
    ).parsed
