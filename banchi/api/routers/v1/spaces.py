import datetime
import io
import typing

from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from loguru import logger
import bson

from banchi.api import models
from banchi.api import schemas
from banchi.api.core import deps

from beanie import PydanticObjectId
from beanie.odm.operators.find import comparison
from beanie.operators import Inc, Set


router = APIRouter(prefix="/spaces", tags=["spaces"])


@router.get("")
async def get_all(
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
    spaces: typing.Annotated[
        models.spaces.Space, Depends(deps.get_current_user_spaces)
    ],
) -> schemas.spaces.SpaceList:
    return dict(spaces=spaces)


@router.post("")
async def create(
    space: schemas.spaces.CreatedSpace,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:
    db_space = await models.spaces.Space.find_one(
        models.spaces.Space.name == space.name,
        models.spaces.Space.owner.id == current_user.id,
        models.spaces.Space.status == "active",
    )
    if db_space:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already space name",
        )

    db_space = await models.spaces.Space.find_one(
        models.spaces.Space.code == space.code,
        models.spaces.Space.status == "active",
        models.spaces.Space.owner.id == current_user.id,
    )
    if db_space:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already space code",
        )

    data = space.dict()
    data["owner"] = current_user
    data["updated_by"] = current_user
    db_space = models.spaces.Space.parse_obj(data)
    await db_space.save()

    db_space_role = models.spaces.SpaceRole(
        added_by=current_user,
        updated_by=current_user,
        member=current_user,
        role="owner",
        space=db_space,
    )
    await db_space_role.save()

    return db_space


@router.get("/{space_id}")
async def get(
    space_id: PydanticObjectId,
    space: typing.Annotated[models.spaces.Space, Depends(deps.get_current_user_space)],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.spaces.Space:
    return space


@router.get("/{space_id}/accounts")
async def get_accounts(
    space_id: PydanticObjectId,
    db_account: typing.Annotated[
        models.accounts.Account, Depends(deps.get_account_by_space)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.accounts.Account:
    return db_account


@router.put("/{space_id}")
async def update(
    space_id: PydanticObjectId,
    space: schemas.spaces.UpdatedSpace,
    db_space: typing.Annotated[
        models.spaces.Space, Depends(deps.get_current_user_space)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:
    data = space.dict()
    await db_space.update(Set(data))

    db_space.updated_date = datetime.datetime.now()
    db_space.updated_by = current_user
    await db_space.save()

    return db_space


@router.delete("/{space_id}")
async def delete(
    space_id: PydanticObjectId,
    db_space: typing.Annotated[
        models.spaces.Space, Depends(deps.get_current_user_space)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:
    db_space.status = "disactive"
    db_space.updated_date = datetime.datetime.now()
    db_space.updated_by = current_user
    await db_space.save()

    return db_space
