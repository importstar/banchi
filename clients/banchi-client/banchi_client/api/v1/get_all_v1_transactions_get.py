import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.transaction_list import TransactionList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    from_account_book_id: Union[None, str],
    to_account_book_id: Union[None, str],
    page: Union[None, Unset, int] = 1,
    size_per_page: Union[None, Unset, int] = 50,
    started_date: Union[None, Unset, datetime.datetime] = UNSET,
    ended_date: Union[None, Unset, datetime.datetime] = UNSET,
    description: Union[None, Unset, str] = UNSET,
    value: Union[None, Unset, float, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_from_account_book_id: Union[None, str]
    json_from_account_book_id = from_account_book_id
    params["from_account_book_id"] = json_from_account_book_id

    json_to_account_book_id: Union[None, str]
    json_to_account_book_id = to_account_book_id
    params["to_account_book_id"] = json_to_account_book_id

    json_page: Union[None, Unset, int]
    if isinstance(page, Unset):
        json_page = UNSET
    else:
        json_page = page
    params["page"] = json_page

    json_size_per_page: Union[None, Unset, int]
    if isinstance(size_per_page, Unset):
        json_size_per_page = UNSET
    else:
        json_size_per_page = size_per_page
    params["size_per_page"] = json_size_per_page

    json_started_date: Union[None, Unset, str]
    if isinstance(started_date, Unset):
        json_started_date = UNSET
    elif isinstance(started_date, datetime.datetime):
        json_started_date = started_date.isoformat()
    else:
        json_started_date = started_date
    params["started_date"] = json_started_date

    json_ended_date: Union[None, Unset, str]
    if isinstance(ended_date, Unset):
        json_ended_date = UNSET
    elif isinstance(ended_date, datetime.datetime):
        json_ended_date = ended_date.isoformat()
    else:
        json_ended_date = ended_date
    params["ended_date"] = json_ended_date

    json_description: Union[None, Unset, str]
    if isinstance(description, Unset):
        json_description = UNSET
    else:
        json_description = description
    params["description"] = json_description

    json_value: Union[None, Unset, float, str]
    if isinstance(value, Unset):
        json_value = UNSET
    else:
        json_value = value
    params["value"] = json_value

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/transactions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TransactionList]]:
    if response.status_code == 200:
        response_200 = TransactionList.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TransactionList]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    from_account_book_id: Union[None, str],
    to_account_book_id: Union[None, str],
    page: Union[None, Unset, int] = 1,
    size_per_page: Union[None, Unset, int] = 50,
    started_date: Union[None, Unset, datetime.datetime] = UNSET,
    ended_date: Union[None, Unset, datetime.datetime] = UNSET,
    description: Union[None, Unset, str] = UNSET,
    value: Union[None, Unset, float, str] = UNSET,
) -> Response[Union[HTTPValidationError, TransactionList]]:
    """Get All

    Args:
        from_account_book_id (Union[None, str]):
        to_account_book_id (Union[None, str]):
        page (Union[None, Unset, int]):  Default: 1.
        size_per_page (Union[None, Unset, int]):  Default: 50.
        started_date (Union[None, Unset, datetime.datetime]):
        ended_date (Union[None, Unset, datetime.datetime]):
        description (Union[None, Unset, str]):
        value (Union[None, Unset, float, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TransactionList]]
    """

    kwargs = _get_kwargs(
        from_account_book_id=from_account_book_id,
        to_account_book_id=to_account_book_id,
        page=page,
        size_per_page=size_per_page,
        started_date=started_date,
        ended_date=ended_date,
        description=description,
        value=value,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    from_account_book_id: Union[None, str],
    to_account_book_id: Union[None, str],
    page: Union[None, Unset, int] = 1,
    size_per_page: Union[None, Unset, int] = 50,
    started_date: Union[None, Unset, datetime.datetime] = UNSET,
    ended_date: Union[None, Unset, datetime.datetime] = UNSET,
    description: Union[None, Unset, str] = UNSET,
    value: Union[None, Unset, float, str] = UNSET,
) -> Optional[Union[HTTPValidationError, TransactionList]]:
    """Get All

    Args:
        from_account_book_id (Union[None, str]):
        to_account_book_id (Union[None, str]):
        page (Union[None, Unset, int]):  Default: 1.
        size_per_page (Union[None, Unset, int]):  Default: 50.
        started_date (Union[None, Unset, datetime.datetime]):
        ended_date (Union[None, Unset, datetime.datetime]):
        description (Union[None, Unset, str]):
        value (Union[None, Unset, float, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TransactionList]
    """

    return sync_detailed(
        client=client,
        from_account_book_id=from_account_book_id,
        to_account_book_id=to_account_book_id,
        page=page,
        size_per_page=size_per_page,
        started_date=started_date,
        ended_date=ended_date,
        description=description,
        value=value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    from_account_book_id: Union[None, str],
    to_account_book_id: Union[None, str],
    page: Union[None, Unset, int] = 1,
    size_per_page: Union[None, Unset, int] = 50,
    started_date: Union[None, Unset, datetime.datetime] = UNSET,
    ended_date: Union[None, Unset, datetime.datetime] = UNSET,
    description: Union[None, Unset, str] = UNSET,
    value: Union[None, Unset, float, str] = UNSET,
) -> Response[Union[HTTPValidationError, TransactionList]]:
    """Get All

    Args:
        from_account_book_id (Union[None, str]):
        to_account_book_id (Union[None, str]):
        page (Union[None, Unset, int]):  Default: 1.
        size_per_page (Union[None, Unset, int]):  Default: 50.
        started_date (Union[None, Unset, datetime.datetime]):
        ended_date (Union[None, Unset, datetime.datetime]):
        description (Union[None, Unset, str]):
        value (Union[None, Unset, float, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TransactionList]]
    """

    kwargs = _get_kwargs(
        from_account_book_id=from_account_book_id,
        to_account_book_id=to_account_book_id,
        page=page,
        size_per_page=size_per_page,
        started_date=started_date,
        ended_date=ended_date,
        description=description,
        value=value,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    from_account_book_id: Union[None, str],
    to_account_book_id: Union[None, str],
    page: Union[None, Unset, int] = 1,
    size_per_page: Union[None, Unset, int] = 50,
    started_date: Union[None, Unset, datetime.datetime] = UNSET,
    ended_date: Union[None, Unset, datetime.datetime] = UNSET,
    description: Union[None, Unset, str] = UNSET,
    value: Union[None, Unset, float, str] = UNSET,
) -> Optional[Union[HTTPValidationError, TransactionList]]:
    """Get All

    Args:
        from_account_book_id (Union[None, str]):
        to_account_book_id (Union[None, str]):
        page (Union[None, Unset, int]):  Default: 1.
        size_per_page (Union[None, Unset, int]):  Default: 50.
        started_date (Union[None, Unset, datetime.datetime]):
        ended_date (Union[None, Unset, datetime.datetime]):
        description (Union[None, Unset, str]):
        value (Union[None, Unset, float, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TransactionList]
    """

    return (
        await asyncio_detailed(
            client=client,
            from_account_book_id=from_account_book_id,
            to_account_book_id=to_account_book_id,
            page=page,
            size_per_page=size_per_page,
            started_date=started_date,
            ended_date=ended_date,
            description=description,
            value=value,
        )
    ).parsed
