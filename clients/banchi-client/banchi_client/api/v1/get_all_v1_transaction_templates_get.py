from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.transaction_template_list import TransactionTemplateList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    account_id: None | str,
    page: int | None | Unset = 1,
    size_per_page: int | None | Unset = 50,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_account_id: None | str
    json_account_id = account_id
    params["account_id"] = json_account_id

    json_page: int | None | Unset
    if isinstance(page, Unset):
        json_page = UNSET
    else:
        json_page = page
    params["page"] = json_page

    json_size_per_page: int | None | Unset
    if isinstance(size_per_page, Unset):
        json_size_per_page = UNSET
    else:
        json_size_per_page = size_per_page
    params["size_per_page"] = json_size_per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/transaction-templates",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TransactionTemplateList | None:
    if response.status_code == 200:
        response_200 = TransactionTemplateList.from_dict(response.json())

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
) -> Response[HTTPValidationError | TransactionTemplateList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    account_id: None | str,
    page: int | None | Unset = 1,
    size_per_page: int | None | Unset = 50,
) -> Response[HTTPValidationError | TransactionTemplateList]:
    """Get All

    Args:
        account_id (None | str):
        page (int | None | Unset):  Default: 1.
        size_per_page (int | None | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TransactionTemplateList]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        page=page,
        size_per_page=size_per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    account_id: None | str,
    page: int | None | Unset = 1,
    size_per_page: int | None | Unset = 50,
) -> HTTPValidationError | TransactionTemplateList | None:
    """Get All

    Args:
        account_id (None | str):
        page (int | None | Unset):  Default: 1.
        size_per_page (int | None | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TransactionTemplateList
    """

    return sync_detailed(
        client=client,
        account_id=account_id,
        page=page,
        size_per_page=size_per_page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    account_id: None | str,
    page: int | None | Unset = 1,
    size_per_page: int | None | Unset = 50,
) -> Response[HTTPValidationError | TransactionTemplateList]:
    """Get All

    Args:
        account_id (None | str):
        page (int | None | Unset):  Default: 1.
        size_per_page (int | None | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TransactionTemplateList]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        page=page,
        size_per_page=size_per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    account_id: None | str,
    page: int | None | Unset = 1,
    size_per_page: int | None | Unset = 50,
) -> HTTPValidationError | TransactionTemplateList | None:
    """Get All

    Args:
        account_id (None | str):
        page (int | None | Unset):  Default: 1.
        size_per_page (int | None | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TransactionTemplateList
    """

    return (
        await asyncio_detailed(
            client=client,
            account_id=account_id,
            page=page,
            size_per_page=size_per_page,
        )
    ).parsed
