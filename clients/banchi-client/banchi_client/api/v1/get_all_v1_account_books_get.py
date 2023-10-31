from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from typing import Union
from typing import Dict
from typing import Union
from ...models.http_validation_error import HTTPValidationError
from ...models.account_book_list import AccountBookList
from ...types import UNSET, Unset


def _get_kwargs(
    *,
    account_id: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    json_account_id: Union[None, Unset, str]
    if isinstance(account_id, Unset):
        json_account_id = UNSET

    else:
        json_account_id = account_id

    params["account_id"] = json_account_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/v1/account-books",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AccountBookList, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AccountBookList.from_dict(response.json())

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
) -> Response[Union[AccountBookList, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    account_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[AccountBookList, HTTPValidationError]]:
    """Get All

    Args:
        account_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountBookList, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    account_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[AccountBookList, HTTPValidationError]]:
    """Get All

    Args:
        account_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountBookList, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        account_id=account_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    account_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[AccountBookList, HTTPValidationError]]:
    """Get All

    Args:
        account_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AccountBookList, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    account_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[AccountBookList, HTTPValidationError]]:
    """Get All

    Args:
        account_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AccountBookList, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            account_id=account_id,
        )
    ).parsed
