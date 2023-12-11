from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.created_space import CreatedSpace
from ...models.http_validation_error import HTTPValidationError
from ...models.space_role import SpaceRole
from ...types import UNSET, Response


def _get_kwargs(
    space_role_id: str,
    *,
    json_body: CreatedSpace,
    spaces_id: str,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    params["spaces_id"] = spaces_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v1/spaces/<space_id>/roles/{space_role_id}/update".format(
            space_role_id=space_role_id,
        ),
        "json": json_json_body,
        "params": params,
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
    space_role_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedSpace,
    spaces_id: str,
) -> Response[Union[HTTPValidationError, SpaceRole]]:
    """Update

    Args:
        space_role_id (str):
        spaces_id (str):
        json_body (CreatedSpace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SpaceRole]]
    """

    kwargs = _get_kwargs(
        space_role_id=space_role_id,
        json_body=json_body,
        spaces_id=spaces_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    space_role_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedSpace,
    spaces_id: str,
) -> Optional[Union[HTTPValidationError, SpaceRole]]:
    """Update

    Args:
        space_role_id (str):
        spaces_id (str):
        json_body (CreatedSpace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SpaceRole]
    """

    return sync_detailed(
        space_role_id=space_role_id,
        client=client,
        json_body=json_body,
        spaces_id=spaces_id,
    ).parsed


async def asyncio_detailed(
    space_role_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedSpace,
    spaces_id: str,
) -> Response[Union[HTTPValidationError, SpaceRole]]:
    """Update

    Args:
        space_role_id (str):
        spaces_id (str):
        json_body (CreatedSpace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SpaceRole]]
    """

    kwargs = _get_kwargs(
        space_role_id=space_role_id,
        json_body=json_body,
        spaces_id=spaces_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    space_role_id: str,
    *,
    client: AuthenticatedClient,
    json_body: CreatedSpace,
    spaces_id: str,
) -> Optional[Union[HTTPValidationError, SpaceRole]]:
    """Update

    Args:
        space_role_id (str):
        spaces_id (str):
        json_body (CreatedSpace):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SpaceRole]
    """

    return (
        await asyncio_detailed(
            space_role_id=space_role_id,
            client=client,
            json_body=json_body,
            spaces_id=spaces_id,
        )
    ).parsed
