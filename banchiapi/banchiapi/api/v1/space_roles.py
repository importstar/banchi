import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status
from loguru import logger
import bson

from banchiapi import models
from banchiapi import schemas
from banchiapi.core import deps

router = APIRouter(prefix="/spaces/<space_id>/roles", tags=["space roles"])


@router.get("")
async def get_all(
    space_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
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


@router.post(
    "/add",
    response_model_by_alias=False,
)
async def add(
    space_id: str,
    space_role: schemas.spaces.CreatedSpace,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.SpaceRole:
    db_space_role = await models.spaces.SpaceRole.find_one(
        models.spaces.SpaceRole.name == space_role.name,
        models.spaces.SpaceRole.status == "active",
    )
    if db_space_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already space_role name",
        )

    db_space_role = await models.spaces.SpaceRole.find_one(
        models.spaces.SpaceRole.code == space_role.code,
        models.spaces.SpaceRole.status == "active",
    )
    if db_space_role:
        raise status.HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already space_role code",
        )

    data = space_role.dict()
    data["owner"] = current_user
    data["updated_by"] = current_user
    db_space_role = models.spaces.SpaceRole.parse_obj(data)
    await db_space_role.save()

    return db_space_role


@router.get(
    "/{space_role_id}",
    response_model_by_alias=False,
)
async def get(
    space_id: str,
    space_role_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.SpaceRole:
    db_space_role = await models.spaces.SpaceRole.find_one(
        models.spaces.SpaceRole.id == bson.ObjectId(space_role_id),
        models.spaces.SpaceRole.owner.id == current_user.id,
        fetch_links=True,
    )

    if not db_space_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this space_role",
        )
    return db_space_role


@router.put(
    "/{space_role_id}/update",
    response_model_by_alias=False,
    response_model=schemas.spaces.SpaceRole,
)
async def update(
    spaces_id: str,
    space_role_id: str,
    space_role: schemas.spaces.CreatedSpace,
    current_user: models.users.User = Depends(deps.get_current_user),
):
    db_space_role = models.Space.objects(id=space_role_id).first()
    if not db_space_role:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    db_space_roles = models.Space.objects(
        name=space_role.name, status="active", id__ne=space_role_id
    )
    if db_space_roles:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already space_role name",
        )
    db_space_roles = models.Space.objects(
        code=space_role.code, status="active", id__ne=space_role_id
    )
    if db_space_roles:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already space_role code",
        )

    data = space_role.dict()
    db_space_role.update(**data)

    db_space_role.updated_date = datetime.datetime.now()
    db_space_role.save()
    db_space_role.reload()
    return db_space_role


@router.delete(
    "/{space_role_id}/delete",
    response_model_by_alias=False,
    response_model=schemas.spaces.SpaceRole,
)
async def delete(
    space_id: str,
    space_role_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
):
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