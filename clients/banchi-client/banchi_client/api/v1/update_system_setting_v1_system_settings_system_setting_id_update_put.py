from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.system_setting_in_response import SystemSettingInResponse
from typing import Dict
from ...models.http_validation_error import HTTPValidationError
from ...models.system_setting_in_create import SystemSettingInCreate


def _get_kwargs(
    system_setting_id: str,
    *,
    json_body: SystemSettingInCreate,
) -> Dict[str, Any]:
    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": "/v1/system_settings/{system_setting_id}/update".format(
            system_setting_id=system_setting_id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SystemSettingInResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SystemSettingInResponse.from_dict(response.json())

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
    json_body: SystemSettingInCreate,
) -> Response[Union[HTTPValidationError, SystemSettingInResponse]]:
    """Update System Setting

    Args:
        system_setting_id (str):
        json_body (SystemSettingInCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SystemSettingInResponse]]
    """

    kwargs = _get_kwargs(
        system_setting_id=system_setting_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    system_setting_id: str,
    *,
    client: AuthenticatedClient,
    json_body: SystemSettingInCreate,
) -> Optional[Union[HTTPValidationError, SystemSettingInResponse]]:
    """Update System Setting

    Args:
        system_setting_id (str):
        json_body (SystemSettingInCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SystemSettingInResponse]
    """

    return sync_detailed(
        system_setting_id=system_setting_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    system_setting_id: str,
    *,
    client: AuthenticatedClient,
    json_body: SystemSettingInCreate,
) -> Response[Union[HTTPValidationError, SystemSettingInResponse]]:
    """Update System Setting

    Args:
        system_setting_id (str):
        json_body (SystemSettingInCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SystemSettingInResponse]]
    """

    kwargs = _get_kwargs(
        system_setting_id=system_setting_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    system_setting_id: str,
    *,
    client: AuthenticatedClient,
    json_body: SystemSettingInCreate,
) -> Optional[Union[HTTPValidationError, SystemSettingInResponse]]:
    """Update System Setting

    Args:
        system_setting_id (str):
        json_body (SystemSettingInCreate):

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
            json_body=json_body,
        )
    ).parsed
