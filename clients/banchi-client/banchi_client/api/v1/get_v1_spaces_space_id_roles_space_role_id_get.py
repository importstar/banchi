from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.space_role import SpaceRole
from ...types import Response


def _get_kwargs(
    space_id: str,
    space_role_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/spaces/{space_id}/roles/{space_role_id}".format(
            space_id=quote(str(space_id), safe=""),
            space_role_id=quote(str(space_role_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | SpaceRole | None:
    if response.status_code == 200:
        response_200 = SpaceRole.from_dict(response.json())

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
) -> Response[HTTPValidationError | SpaceRole]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    space_id: str,
    space_role_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | SpaceRole]:
    """Get

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        space_role_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SpaceRole]
    """

    kwargs = _get_kwargs(
        space_id=space_id,
        space_role_id=space_role_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    space_id: str,
    space_role_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | SpaceRole | None:
    """Get

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        space_role_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SpaceRole
    """

    return sync_detailed(
        space_id=space_id,
        space_role_id=space_role_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    space_id: str,
    space_role_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | SpaceRole]:
    """Get

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        space_role_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SpaceRole]
    """

    kwargs = _get_kwargs(
        space_id=space_id,
        space_role_id=space_role_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    space_id: str,
    space_role_id: str,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | SpaceRole | None:
    """Get

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        space_role_id (str):  Example: 5eb7cf5a86d9755df3a6c593.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SpaceRole
    """

    return (
        await asyncio_detailed(
            space_id=space_id,
            space_role_id=space_role_id,
            client=client,
        )
    ).parsed
