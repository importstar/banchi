from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.user_list import UserList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    first_name: Union[Unset, str] = "",
    last_name: Union[Unset, str] = "",
    citizen_id: Union[Unset, str] = "",
    current_page: Union[Unset, int] = 1,
    limit: Union[Unset, int] = 50,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["first_name"] = first_name

    params["last_name"] = last_name

    params["citizen_id"] = citizen_id

    params["current_page"] = current_page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/v1/users",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, UserList]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UserList.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, UserList]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    first_name: Union[Unset, str] = "",
    last_name: Union[Unset, str] = "",
    citizen_id: Union[Unset, str] = "",
    current_page: Union[Unset, int] = 1,
    limit: Union[Unset, int] = 50,
) -> Response[Union[HTTPValidationError, UserList]]:
    """Get All

    Args:
        first_name (Union[Unset, str]):  Default: ''.
        last_name (Union[Unset, str]):  Default: ''.
        citizen_id (Union[Unset, str]):  Default: ''.
        current_page (Union[Unset, int]):  Default: 1.
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserList]]
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
    first_name: Union[Unset, str] = "",
    last_name: Union[Unset, str] = "",
    citizen_id: Union[Unset, str] = "",
    current_page: Union[Unset, int] = 1,
    limit: Union[Unset, int] = 50,
) -> Optional[Union[HTTPValidationError, UserList]]:
    """Get All

    Args:
        first_name (Union[Unset, str]):  Default: ''.
        last_name (Union[Unset, str]):  Default: ''.
        citizen_id (Union[Unset, str]):  Default: ''.
        current_page (Union[Unset, int]):  Default: 1.
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserList]
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
    first_name: Union[Unset, str] = "",
    last_name: Union[Unset, str] = "",
    citizen_id: Union[Unset, str] = "",
    current_page: Union[Unset, int] = 1,
    limit: Union[Unset, int] = 50,
) -> Response[Union[HTTPValidationError, UserList]]:
    """Get All

    Args:
        first_name (Union[Unset, str]):  Default: ''.
        last_name (Union[Unset, str]):  Default: ''.
        citizen_id (Union[Unset, str]):  Default: ''.
        current_page (Union[Unset, int]):  Default: 1.
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserList]]
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
    first_name: Union[Unset, str] = "",
    last_name: Union[Unset, str] = "",
    citizen_id: Union[Unset, str] = "",
    current_page: Union[Unset, int] = 1,
    limit: Union[Unset, int] = 50,
) -> Optional[Union[HTTPValidationError, UserList]]:
    """Get All

    Args:
        first_name (Union[Unset, str]):  Default: ''.
        last_name (Union[Unset, str]):  Default: ''.
        citizen_id (Union[Unset, str]):  Default: ''.
        current_page (Union[Unset, int]):  Default: 1.
        limit (Union[Unset, int]):  Default: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserList]
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
