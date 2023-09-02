import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status
from loguru import logger
from banchiapi import models
from banchiapi import schemas
from banchiapi.core import deps

router = APIRouter(prefix="/spaces", tags=["space"])


@router.get("/", response_model_by_alias=False)
async def get_spaces(
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.SpaceList:
    spaces = await models.spaces.Space.find(
        models.spaces.Space.status == "active"
    ).to_list()
    print("-->", spaces)

    return dict(spaces=spaces)


@router.post(
    "/create",
    response_model_by_alias=False,
)
async def create_space(
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already space code",
        )

    data = space.dict()
    data["owner"] = current_user
    data["updated_by"] = current_user
    db_space = models.spaces.Space(**data)
    print("->", db_space.dict())
    await db_space.insert()

    return db_space


@router.get(
    "/{space_id}",
    response_model_by_alias=False,
    response_model=schemas.spaces.Space,
)
def get_space(
    space_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
):
    try:
        db_space = models.Space.objects.get(id=space_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this space",
        )
    return db_space


@router.put(
    "/{space_id}/update",
    response_model_by_alias=False,
    response_model=schemas.spaces.Space,
)
def update_space(
    space_id: str,
    space: schemas.spaces.CreatedSpace,
    current_user: models.users.User = Depends(deps.get_current_user),
):
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
    "/{space_id}/delete",
    response_model_by_alias=False,
    response_model=schemas.spaces.Space,
)
def delete_space(
    space_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
):
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
