from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.created_transaction_template import CreatedTransactionTemplate
from ...models.http_validation_error import HTTPValidationError
from ...models.transaction_template import TransactionTemplate
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: CreatedTransactionTemplate,
    account_id: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["account_id"] = account_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/transaction-templates",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    *,
    client: AuthenticatedClient,
    body: CreatedTransactionTemplate,
    account_id: str,
) -> Response[HTTPValidationError | TransactionTemplate]:
    """Create

    Args:
        account_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (CreatedTransactionTemplate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TransactionTemplate]
    """

    kwargs = _get_kwargs(
        body=body,
        account_id=account_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreatedTransactionTemplate,
    account_id: str,
) -> HTTPValidationError | TransactionTemplate | None:
    """Create

    Args:
        account_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (CreatedTransactionTemplate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TransactionTemplate
    """

    return sync_detailed(
        client=client,
        body=body,
        account_id=account_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreatedTransactionTemplate,
    account_id: str,
) -> Response[HTTPValidationError | TransactionTemplate]:
    """Create

    Args:
        account_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (CreatedTransactionTemplate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TransactionTemplate]
    """

    kwargs = _get_kwargs(
        body=body,
        account_id=account_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreatedTransactionTemplate,
    account_id: str,
) -> HTTPValidationError | TransactionTemplate | None:
    """Create

    Args:
        account_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (CreatedTransactionTemplate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TransactionTemplate
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            account_id=account_id,
        )
    ).parsed
