from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.user_list import UserList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    first_name: str | Unset = "",
    last_name: str | Unset = "",
    citizen_id: str | Unset = "",
    current_page: int | Unset = 1,
    limit: int | Unset = 50,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["first_name"] = first_name

    params["last_name"] = last_name

    params["citizen_id"] = citizen_id

    params["current_page"] = current_page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/users",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | UserList | None:
    if response.status_code == 200:
        response_200 = UserList.from_dict(response.json())

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
) -> Response[HTTPValidationError | UserList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    first_name: str | Unset = "",
    last_name: str | Unset = "",
    citizen_id: str | Unset = "",
    current_page: int | Unset = 1,
    limit: int | Unset = 50,
) -> Response[HTTPValidationError | UserList]:
    """Get All

    Args:
        first_name (str | Unset):  Default: ''.
        last_name (str | Unset):  Default: ''.
        citizen_id (str | Unset):  Default: ''.
        current_page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UserList]
    """

    kwargs = _get_kwargs(
        first_name=first_name,
        last_name=last_name,
        citizen_id=citizen_id,
        current_page=current_page,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    first_name: str | Unset = "",
    last_name: str | Unset = "",
    citizen_id: str | Unset = "",
    current_page: int | Unset = 1,
    limit: int | Unset = 50,
) -> HTTPValidationError | UserList | None:
    """Get All

    Args:
        first_name (str | Unset):  Default: ''.
        last_name (str | Unset):  Default: ''.
        citizen_id (str | Unset):  Default: ''.
        current_page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UserList
    """

    return sync_detailed(
        client=client,
        first_name=first_name,
        last_name=last_name,
        citizen_id=citizen_id,
        current_page=current_page,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    first_name: str | Unset = "",
    last_name: str | Unset = "",
    citizen_id: str | Unset = "",
    current_page: int | Unset = 1,
    limit: int | Unset = 50,
) -> Response[HTTPValidationError | UserList]:
    """Get All

    Args:
        first_name (str | Unset):  Default: ''.
        last_name (str | Unset):  Default: ''.
        citizen_id (str | Unset):  Default: ''.
        current_page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UserList]
    """

    kwargs = _get_kwargs(
        first_name=first_name,
        last_name=last_name,
        citizen_id=citizen_id,
        current_page=current_page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    first_name: str | Unset = "",
    last_name: str | Unset = "",
    citizen_id: str | Unset = "",
    current_page: int | Unset = 1,
    limit: int | Unset = 50,
) -> HTTPValidationError | UserList | None:
    """Get All

    Args:
        first_name (str | Unset):  Default: ''.
        last_name (str | Unset):  Default: ''.
        citizen_id (str | Unset):  Default: ''.
        current_page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UserList
    """

    return (
        await asyncio_detailed(
            client=client,
            first_name=first_name,
            last_name=last_name,
            citizen_id=citizen_id,
            current_page=current_page,
            limit=limit,
        )
    ).parsed
