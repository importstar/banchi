from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.space_role_list import SpaceRoleList
from ...types import Response


def _get_kwargs(
    space_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/v1/spaces/{space_id}/roles",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SpaceRoleList]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SpaceRoleList.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SpaceRoleList]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    space_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, SpaceRoleList]]:
    """Get All

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SpaceRoleList]]
    """

    kwargs = _get_kwargs(
        space_id=space_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    space_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, SpaceRoleList]]:
    """Get All

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SpaceRoleList]
    """

    return sync_detailed(
        space_id=space_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    space_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, SpaceRoleList]]:
    """Get All

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SpaceRoleList]]
    """

    kwargs = _get_kwargs(
        space_id=space_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    space_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, SpaceRoleList]]:
    """Get All

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SpaceRoleList]
    """

    return (
        await asyncio_detailed(
            space_id=space_id,
            client=client,
        )
    ).parsed
