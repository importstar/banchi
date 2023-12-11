import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status
from loguru import logger
import bson

from banchiapi import models
from banchiapi import schemas
from banchiapi.core import deps

from beanie import PydanticObjectId
from beanie.odm.operators.find import comparison


router = APIRouter(prefix="/spaces", tags=["spaces"])


@router.get("", response_model_by_alias=False)
async def get_all(
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.SpaceList:
    space_roles = await models.spaces.SpaceRole.find(
        models.spaces.SpaceRole.member.id == current_user.id,
        models.spaces.SpaceRole.status == "active",
        fetch_links=True,
    ).to_list()

    spaces = await models.spaces.Space.find(
        comparison.In(
            models.spaces.Space.id, [space_role.space.id for space_role in space_roles]
        ),
        models.spaces.Space.status == "active",
        fetch_links=True,
    ).to_list()

    return dict(spaces=spaces)

    # spaces = []

    # for space_role in space_roles:
    #     subspaces = await models.spaces.Space.find(
    #         models.spaces.Space.id == space_role.space.id,
    #         models.spaces.Space.status == "active",
    #         fetch_links=True,
    #     ).to_list()
    #     spaces.extend(subspaces)

    # return dict(spaces=spaces)


@router.post(
    "",
)
async def create(
    space: schemas.spaces.CreatedSpace,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:
    db_space = await models.spaces.Space.find_one(
        models.spaces.Space.name == space.name, models.spaces.Space.status == "active"
    )
    if db_space:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already space name",
        )

    db_space = await models.spaces.Space.find_one(
        models.spaces.Space.code == space.code, models.spaces.Space.status == "active"
    )
    if db_space:
        raise status.HTTPException(
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


@router.get(
    "/{space_id}",
)
async def get(
    space_id: PydanticObjectId,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:
    db_space = await models.spaces.Space.find_one(
        models.spaces.Space.id == space_id,
        models.spaces.Space.owner.id == current_user.id,
        fetch_links=True,
    )

    if not db_space:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this space",
        )
    return db_space


@router.put(
    "/{space_id}",
)
async def update(
    space_id: PydanticObjectId,
    space: schemas.spaces.CreatedSpace,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:
    db_space = models.Space.objects(id=space_id).first()
    if not db_space:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    db_spaces = models.Space.objects(name=space.name, status="active", id__ne=space_id)
    if db_spaces:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already space name",
        )
    db_spaces = models.Space.objects(code=space.code, status="active", id__ne=space_id)
    if db_spaces:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already space code",
        )

    data = space.dict()
    db_space.update(**data)

    db_space.updated_date = datetime.datetime.now()
    db_space.save()
    db_space.reload()
    return db_space


@router.delete(
    "/{space_id}",
)
async def delete(
    space_id: PydanticObjectId,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:
    try:
        db_space = models.Space.objects.get(id=space_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this space",
        )
    db_space.update(status="disactive", updated_date=datetime.datetime.now())
    db_space.reload()
    db_space.save()

    divisions = models.Division.objects(space=db_space, status="active")
    for division in divisions:
        division.status = "disactive"
        division.save()
    return db_space
