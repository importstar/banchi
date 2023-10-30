from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.user import User
from ...models.http_validation_error import HTTPValidationError
from typing import Dict


def _get_kwargs(
    user_id: str,
    *,
    role: str,
    action: str,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    params["role"] = role

    params["action"] = action

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
        "url": "/v1/users/{user_id}/set_role".format(
            user_id=user_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, User]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = User.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, User]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: AuthenticatedClient,
    role: str,
    action: str,
) -> Response[Union[HTTPValidationError, User]]:
    """Set Role

    Args:
        user_id (str):
        role (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, User]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        role=role,
        action=action,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: AuthenticatedClient,
    role: str,
    action: str,
) -> Optional[Union[HTTPValidationError, User]]:
    """Set Role

    Args:
        user_id (str):
        role (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, User]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        role=role,
        action=action,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: AuthenticatedClient,
    role: str,
    action: str,
) -> Response[Union[HTTPValidationError, User]]:
    """Set Role

    Args:
        user_id (str):
        role (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, User]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        role=role,
        action=action,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: AuthenticatedClient,
    role: str,
    action: str,
) -> Optional[Union[HTTPValidationError, User]]:
    """Set Role

    Args:
        user_id (str):
        role (str):
        action (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, User]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            role=role,
            action=action,
        )
    ).parsed
