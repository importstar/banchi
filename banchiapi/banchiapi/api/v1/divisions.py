import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST
from loguru import logger
from banchaiapi import models
from banchaiapi.core import deps
from banchaiapi.schemas.divisions import (
    DivisionInResponse,
    DivisionInCreate,
    DivisionInUpdate,
    ListDivisionInResponse,
)
from banchaiapi.schemas.system_settings import (
    AuthorizedSignatoryInCreate,
    AuthorizedSignatoryInUpdate,
)

router = APIRouter(prefix="/divisions", tags=["divisions"])


@router.get(
    "/",
    response_model_by_alias=False,
    response_model=ListDivisionInResponse,
)
def get_divisions(
    organization_id: str = "",
    name: str = "",
    current_user: models.User = Depends(deps.get_current_user),
    current_page: int = 1,
    limit: int = 50,
):
    divisions = []
    count = 0
    is_search = False

    if organization_id:
        organization = models.Organization.objects(id=organization_id).first()
        if not organization:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Not found this organization",
            )
        if divisions:
            divisions = divisions.filter(organization=organization)
        elif not is_search:
            divisions = models.Division.objects(
                status="active", organization=organization
            ).order_by("-created_date")
        is_search = True

    if name:
        if divisions:
            divisions = divisions.filter(name__contains=name)
        elif not is_search:
            divisions = models.Division.objects(
                name__contains=name, status="active"
            ).order_by("-created_date")

        is_search = True

    if divisions:
        count = divisions.count()
        divisions = divisions.skip((current_page - 1) * limit).limit(limit)

    elif not is_search:
        count = models.Division.objects(status="active").count()
        divisions = (
            models.Division.objects(status="active")
            .order_by("-created_date")
            .skip((current_page - 1) * limit)
            .limit(limit)
        )

    if count % limit == 0 and count // limit > 0:
        total_page = count // limit
    else:
        total_page = (count // limit) + 1

    return ListDivisionInResponse(
        divisions=list(divisions),
        count=count,
        current_page=current_page,
        total_page=total_page,
    )


@router.post(
    "/create",
    response_model_by_alias=False,
    response_model=DivisionInResponse,
)
def create_disivion(
    division: DivisionInCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    organization = models.Organization.objects(id=division.organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this organization",
        )
    db_division = models.Division.objects(
        name=division.name, status="active", organization=organization
    ).first()
    if db_division:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already division name",
        )
    db_division = models.Division.objects(
        code=division.code, status="active", organization=organization
    ).first()
    if db_division:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already division code",
        )

    data = division.dict()
    del data["organization_id"]
    db_division = models.Division(**data)
    db_division.organization = organization
    db_division.created_date = datetime.datetime.now()
    db_division.updated_date = datetime.datetime.now()
    db_division.save()

    return db_division


@router.get(
    "/{division_id}",
    response_model_by_alias=False,
    response_model=DivisionInResponse,
)
def get_division(
    division_id: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        db_division = models.Division.objects.get(id=division_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this division",
        )
    return db_division


@router.put(
    "/{division_id}/update",
    response_model_by_alias=False,
    response_model=DivisionInResponse,
)
def update_division(
    division_id: str,
    division: DivisionInUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_division = models.Division.objects(id=division_id).first()
    if not db_division:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    db_divisions = models.Division.objects(
        name=division.name,
        status="active",
        id__ne=division_id,
        organization=db_division.organization,
    )
    if db_divisions:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already division name",
        )
    db_divisions = models.Division.objects(
        code=division.code,
        status="active",
        id__ne=division_id,
        organization=db_division.organization,
    )
    if db_divisions:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already division code",
        )
    division_dict = division.dict()
    set_dict = {f"set__{k}": v for k, v in division_dict.items() if v is not None}

    costs = []
    for c in set_dict["set__costs"]:
        cost = models.DivisionCost(
            name=c["name"], price_per_unit=c["price_per_unit"], unit_name=c["unit_name"]
        )
        costs.append(cost)
    db_division.costs = costs
    del set_dict["set__costs"]
    db_division.update(**set_dict)
    db_division.updated_date = datetime.datetime.now()
    db_division.save()
    db_division.reload()
    return db_division


@router.delete(
    "/{division_id}/delete",
    response_model_by_alias=False,
    response_model=DivisionInResponse,
)
def delete_division(
    division_id: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        db_division = models.Division.objects.get(id=division_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this division",
        )
    db_division.update(status="disactive", updated_date=datetime.datetime.now())
    db_division.reload()
    db_division.save()
    return db_division


@router.post(
    "/{division_id}/create_authorized_signatory",
    response_model_by_alias=False,
    response_model=DivisionInResponse,
)
def create_division_authorized_signatory(
    division_id: str,
    authorized_signatory: AuthorizedSignatoryInCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_division = models.Division.objects(id=division_id).first()
    if not db_division:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not Found this division.",
        )

    signature = models.AuthorizedSignatory()
    signature.first_name = authorized_signatory.first_name
    signature.last_name = authorized_signatory.last_name
    signature.role = authorized_signatory.role
    signature.instead = authorized_signatory.instead
    db_division.authorized_signatories.append(signature)
    db_division.updated_date = datetime.datetime.now()
    db_division.save()

    return db_division


@router.delete(
    "/{division_id}/delete_authorized_signatory/{authorized_signatory_id}",
    response_model_by_alias=False,
    response_model=DivisionInResponse,
)
def delete_division_authorized_signatory(
    division_id: str,
    authorized_signatory_id: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_division = models.Division.objects(id=division_id).first()
    if not db_division:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not Found this division.",
        )

    for authorized_signatory in db_division.authorized_signatories:
        if str(authorized_signatory.uid) == authorized_signatory_id:
            db_division.authorized_signatories.remove(authorized_signatory)
            break

    db_division.updated_date = datetime.datetime.now()
    db_division.save()

    return db_division


@router.put(
    "/{division_id}/update_authorized_signatory/{authorized_signatory_id}",
    response_model_by_alias=False,
    response_model=DivisionInResponse,
)
def update_division_authorized_signatory(
    division_id: str,
    authorized_signatory_id: str,
    authorized_signatory: AuthorizedSignatoryInUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_division = models.Division.objects(id=division_id).first()
    if not db_division:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not Found this division.",
        )
    authorized_signatory_dict = authorized_signatory.dict()
    set_dict = {
        f"set__authorized_signatories__S__{k}": v
        for k, v in authorized_signatory_dict.items()
        if v is not None
    }
    authorized_signatory = models.Division.objects(
        id=division_id, authorized_signatories__uid=authorized_signatory_id
    )
    authorized_signatory.update(**set_dict)
    db_division.save()
    db_division.reload()

    return db_division
