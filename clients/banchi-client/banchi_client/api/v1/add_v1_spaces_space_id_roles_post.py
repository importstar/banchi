from http import HTTPStatus
from typing import Any, Dict, Optional, Union

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
    json_body: CreatedSpaceRole,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/v1/spaces/{space_id}/roles".format(
            space_id=space_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SpaceRole]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SpaceRole.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SpaceRole]]:
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
    json_body: CreatedSpaceRole,
) -> Response[Union[HTTPValidationError, SpaceRole]]:
    """Add

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        json_body (CreatedSpaceRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SpaceRole]]
    """

    kwargs = _get_kwargs(
        space_id=space_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    space_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedSpaceRole,
) -> Optional[Union[HTTPValidationError, SpaceRole]]:
    """Add

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        json_body (CreatedSpaceRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SpaceRole]
    """

    return sync_detailed(
        space_id=space_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    space_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedSpaceRole,
) -> Response[Union[HTTPValidationError, SpaceRole]]:
    """Add

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        json_body (CreatedSpaceRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SpaceRole]]
    """

    kwargs = _get_kwargs(
        space_id=space_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    space_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedSpaceRole,
) -> Optional[Union[HTTPValidationError, SpaceRole]]:
    """Add

    Args:
        space_id (str):  Example: 5eb7cf5a86d9755df3a6c593.
        json_body (CreatedSpaceRole):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SpaceRole]
    """

    return (
        await asyncio_detailed(
            space_id=space_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
