import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status
from loguru import logger
import bson
from beanie import PydanticObjectId
import typing

from banchiapi import models
from banchiapi import schemas
from banchiapi.core import deps

router = APIRouter(prefix="/spaces/{space_id}/roles", tags=["space roles"])


@router.get("")
async def get_all(
    space_id: PydanticObjectId,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.spaces.SpaceRoleList:
    space = await models.spaces.Space.get(space_id)

    query_args = [
        models.spaces.SpaceRole.status == "active",
        models.spaces.SpaceRole.space.id == space.id,
    ]

    space_roles = await models.spaces.SpaceRole.find(
        *query_args, fetch_links=True
    ).to_list()

    return dict(space_roles=space_roles)


@router.post("")
async def add(
    space_id: PydanticObjectId,
    space_role: schemas.spaces.CreatedSpaceRole,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.spaces.SpaceRole:
    db_space_role = await models.spaces.SpaceRole.find_one(
        models.spaces.SpaceRole.member.id == space_role.member_id,
        models.spaces.SpaceRole.status == "active",
    )
    if db_space_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already space_role name",
        )

    data = space_role.dict()
    data["added_by"] = current_user
    data["updated_by"] = current_user
    data["member"] = await models.users.User.get(space_role.member_id)
    data["space"] = await models.spaces.Space.get(space_id)
    db_space_role = models.spaces.SpaceRole.parse_obj(data)
    await db_space_role.save()

    return db_space_role


@router.get("/{space_role_id}")
async def get(
    space_id: PydanticObjectId,
    space_role_id: PydanticObjectId,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.spaces.SpaceRole:
    db_space_role = await models.spaces.SpaceRole.find_one(
        models.spaces.SpaceRole.id == space_role_id,
        fetch_links=True,
    )

    if not db_space_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this space_role",
        )
    return db_space_role


@router.put("/{space_role_id}")
async def update(
    space_id: PydanticObjectId,
    space_role_id: PydanticObjectId,
    space_role: schemas.spaces.UpdatedSpaceRole,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.spaces.SpaceRole:
    db_space = await models.spaces.Space.get(space_id)
    if not db_space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )

    db_space_role = await models.spaces.SpaceRole.get(space_role_id, fetch_links=True)
    if not db_space_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    data = space_role.dict()
    db_space_role.role = space_role.role

    db_space_role.updated_date = datetime.datetime.now()
    db_space_role.updated_by = current_user
    await db_space_role.save()

    return db_space_role


@router.delete(
    "/{space_role_id}",
)
async def delete(
    space_id: PydanticObjectId,
    space_role_id: PydanticObjectId,
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.spaces.SpaceRole:
    try:
        db_space_role = models.Space.objects.get(id=space_role_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this space_role",
        )
    db_space_role.update(status="disactive", updated_date=datetime.datetime.now())
    db_space_role.reload()
    db_space_role.save()

    divisions = models.Division.objects(space_role=db_space_role, status="active")
    for division in divisions:
        division.status = "disactive"
        division.save()
    return db_space_role
