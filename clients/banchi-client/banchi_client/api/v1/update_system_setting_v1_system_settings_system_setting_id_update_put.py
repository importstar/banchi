from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.system_setting_in_create import SystemSettingInCreate
from ...models.system_setting_in_response import SystemSettingInResponse
from ...types import Response


def _get_kwargs(
    system_setting_id: str,
    *,
    body: SystemSettingInCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1/system_settings/{system_setting_id}/update",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SystemSettingInResponse]]:
    if response.status_code == 200:
        response_200 = SystemSettingInResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, SystemSettingInResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    system_setting_id: str,
    *,
    client: AuthenticatedClient,
    body: SystemSettingInCreate,
) -> Response[Union[HTTPValidationError, SystemSettingInResponse]]:
    """Update System Setting

    Args:
        system_setting_id (str):
        body (SystemSettingInCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SystemSettingInResponse]]
    """

    kwargs = _get_kwargs(
        system_setting_id=system_setting_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    system_setting_id: str,
    *,
    client: AuthenticatedClient,
    body: SystemSettingInCreate,
) -> Optional[Union[HTTPValidationError, SystemSettingInResponse]]:
    """Update System Setting

    Args:
        system_setting_id (str):
        body (SystemSettingInCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SystemSettingInResponse]
    """

    return sync_detailed(
        system_setting_id=system_setting_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    system_setting_id: str,
    *,
    client: AuthenticatedClient,
    body: SystemSettingInCreate,
) -> Response[Union[HTTPValidationError, SystemSettingInResponse]]:
    """Update System Setting

    Args:
        system_setting_id (str):
        body (SystemSettingInCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SystemSettingInResponse]]
    """

    kwargs = _get_kwargs(
        system_setting_id=system_setting_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    system_setting_id: str,
    *,
    client: AuthenticatedClient,
    body: SystemSettingInCreate,
) -> Optional[Union[HTTPValidationError, SystemSettingInResponse]]:
    """Update System Setting

    Args:
        system_setting_id (str):
        body (SystemSettingInCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SystemSettingInResponse]
    """

    return (
        await asyncio_detailed(
            system_setting_id=system_setting_id,
            client=client,
            body=body,
        )
    ).parsed
