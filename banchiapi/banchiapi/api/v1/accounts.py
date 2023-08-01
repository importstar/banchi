import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST
from loguru import logger
from banchiapi import models
from banchiapi.core import deps
from banchiapi.schemas.spaces import (
    SpaceInResponse,
    SpaceInCreate,
    ListSpaceInResponse,
)
from banchiapi.schemas.system_settings import (
    AuthorizedSignatoryInCreate,
    AuthorizedSignatoryInUpdate,
)

router = APIRouter(prefix="/accounts", tags=["account"])


@router.get(
    "/",
    response_model_by_alias=False,
    response_model=ListSpaceInResponse,
)
def get_spaces(
    name: str = "",
    current_user: models.User = Depends(deps.get_current_user),
    current_page: int = 1,
    limit: int = 50,
):
    spaces = []
    count = 0
    is_search = False

    if name:
        if spaces:
            spaces = spaces.filter(name__contains=name)
        elif not is_search:
            spaces = models.Space.objects(
                name__contains=name, status="active"
            ).order_by("-created_date")

        is_search = True
    if spaces:
        count = spaces.count()
        spaces = spaces.skip((current_page - 1) * limit).limit(limit)

    elif not is_search:
        # count = models.WaterBill.objects().count()
        # water_bills = (
        #     models.WaterBill.objects().skip((current_page - 1) * limit).limit(limit)
        # )
        count = models.Space.objects(status="active").count()
        spaces = (
            models.Space.objects(status="active")
            .order_by("-created_date")
            .skip((current_page - 1) * limit)
            .limit(limit)
        )

    if count % limit == 0 and count // limit > 0:
        total_page = count // limit
    else:
        total_page = (count // limit) + 1
    return ListSpaceInResponse(
        count=count,
        spaces=list(spaces),
        current_page=current_page,
        total_page=total_page,
    )


@router.post(
    "/create",
    response_model_by_alias=False,
    response_model=SpaceInResponse,
)
def create_space(
    space: SpaceInCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_space = models.Space.objects(name=space.name, status="active").first()
    if db_space:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already space name",
        )
    db_space = models.Space.objects(code=space.code, status="active").first()
    if db_space:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already space code",
        )

    data = space.dict()
    db_space = models.Space(**data)
    db_space.created_date = datetime.datetime.now()
    db_space.updated_date = datetime.datetime.now()
    db_space.save()

    return db_space


@router.get(
    "/{space_id}",
    response_model_by_alias=False,
    response_model=SpaceInResponse,
)
def get_space(
    space_id: str,
    current_user: models.User = Depends(deps.get_current_user),
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
    response_model=SpaceInResponse,
)
def update_space(
    space_id: str,
    space: SpaceInCreate,
    current_user: models.User = Depends(deps.get_current_user),
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
    response_model=SpaceInResponse,
)
def delete_space(
    space_id: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        db_space = models.Space.objects.get(id=space_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
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


@router.post(
    "/{space_id}/create_authorized_signatory",
    response_model_by_alias=False,
    response_model=SpaceInResponse,
)
def create_space_authorized_signatory(
    space_id: str,
    authorized_signatory: AuthorizedSignatoryInCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_space = models.Space.objects(id=space_id).first()
    if not db_space:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not Found this space.",
        )

    signature = models.AuthorizedSignatory()
    signature.first_name = authorized_signatory.first_name
    signature.last_name = authorized_signatory.last_name
    signature.role = authorized_signatory.role
    signature.instead = authorized_signatory.instead
    db_space.authorized_signatories.append(signature)
    db_space.updated_date = datetime.datetime.now()
    db_space.save()

    return db_space


@router.delete(
    "/{space_id}/delete_authorized_signatory/{authorized_signatory_id}",
    response_model_by_alias=False,
    response_model=SpaceInResponse,
)
def delete_space_authorized_signatory(
    space_id: str,
    authorized_signatory_id: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_space = models.Space.objects(id=space_id).first()
    if not db_space:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not Found this space.",
        )

    for authorized_signatory in db_space.authorized_signatories:
        if str(authorized_signatory.uid) == authorized_signatory_id:
            db_space.authorized_signatories.remove(authorized_signatory)
            break

    db_space.updated_date = datetime.datetime.now()
    db_space.save()

    return db_space


@router.put(
    "/{space_id}/update_authorized_signatory/{authorized_signatory_id}",
    response_model_by_alias=False,
    response_model=SpaceInResponse,
)
def update_space_authorized_signatory(
    space_id: str,
    authorized_signatory_id: str,
    authorized_signatory: AuthorizedSignatoryInUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_space = models.Space.objects(id=space_id).first()
    if not db_space:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not Found this space.",
        )
    authorized_signatory_dict = authorized_signatory.dict()
    set_dict = {
        f"set__authorized_signatories__S__{k}": v
        for k, v in authorized_signatory_dict.items()
        if v is not None
    }
    authorized_signatory = models.Space.objects(
        id=space_id, authorized_signatories__uid=authorized_signatory_id
    )
    authorized_signatory.update(**set_dict)
    db_space.save()
    db_space.reload()

    return db_space
