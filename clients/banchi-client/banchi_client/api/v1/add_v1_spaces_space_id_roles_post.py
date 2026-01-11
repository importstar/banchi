from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.created_space_role import CreatedSpaceRole
from ...models.http_validation_error import HTTPValidationError
from ...models.space_role import SpaceRole
from ...types import Response


def _get_kwargs(
    space_id: str,
    *,
    body: CreatedSpaceRole,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/spaces/{space_id}/roles".format(
            space_id=quote(str(space_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    *,
    client: AuthenticatedClient,
    body: CreatedSpaceRole,
) -> Response[HTTPValidationError | SpaceRole]:
    """Add

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (CreatedSpaceRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SpaceRole]
    """

    kwargs = _get_kwargs(
        space_id=space_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    space_id: str,
    *,
    client: AuthenticatedClient,
    body: CreatedSpaceRole,
) -> HTTPValidationError | SpaceRole | None:
    """Add

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (CreatedSpaceRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SpaceRole
    """

    return sync_detailed(
        space_id=space_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    space_id: str,
    *,
    client: AuthenticatedClient,
    body: CreatedSpaceRole,
) -> Response[HTTPValidationError | SpaceRole]:
    """Add

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (CreatedSpaceRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SpaceRole]
    """

    kwargs = _get_kwargs(
        space_id=space_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    space_id: str,
    *,
    client: AuthenticatedClient,
    body: CreatedSpaceRole,
) -> HTTPValidationError | SpaceRole | None:
    """Add

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        body (CreatedSpaceRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SpaceRole
    """

    return (
        await asyncio_detailed(
            space_id=space_id,
            client=client,
            body=body,
        )
    ).parsed
