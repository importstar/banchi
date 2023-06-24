import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST
from loguru import logger
from banchaiapi import models
from banchaiapi.core import deps
from banchaiapi.schemas.divisions import (
    DivisionInResponse,
)
from banchaiapi.schemas.organizations import (
    OrganizationInResponse,
    OrganizationInCreate,
    ListOrganizationInResponse,
)
from banchaiapi.schemas.system_settings import (
    AuthorizedSignatoryInCreate,
    AuthorizedSignatoryInUpdate,
)

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get(
    "/",
    response_model_by_alias=False,
    response_model=ListOrganizationInResponse,
)
def get_organizations(
    name: str = "",
    current_user: models.User = Depends(deps.get_current_user),
    current_page: int = 1,
    limit: int = 50,
):
    organizations = []
    count = 0
    is_search = False

    if name:
        if organizations:
            organizations = organizations.filter(name__contains=name)
        elif not is_search:
            organizations = models.Organization.objects(
                name__contains=name, status="active"
            ).order_by("-created_date")

        is_search = True
    if organizations:
        count = organizations.count()
        organizations = organizations.skip((current_page - 1) * limit).limit(limit)

    elif not is_search:
        # count = models.WaterBill.objects().count()
        # water_bills = (
        #     models.WaterBill.objects().skip((current_page - 1) * limit).limit(limit)
        # )
        count = models.Organization.objects(status="active").count()
        organizations = (
            models.Organization.objects(status="active")
            .order_by("-created_date")
            .skip((current_page - 1) * limit)
            .limit(limit)
        )

    if count % limit == 0 and count // limit > 0:
        total_page = count // limit
    else:
        total_page = (count // limit) + 1
    return ListOrganizationInResponse(
        count=count,
        organizations=list(organizations),
        current_page=current_page,
        total_page=total_page,
    )


@router.post(
    "/create",
    response_model_by_alias=False,
    response_model=OrganizationInResponse,
)
def create_organization(
    organization: OrganizationInCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_organization = models.Organization.objects(
        name=organization.name, status="active"
    ).first()
    if db_organization:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already organization name",
        )
    db_organization = models.Organization.objects(
        code=organization.code, status="active"
    ).first()
    if db_organization:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already organization code",
        )

    data = organization.dict()
    db_organization = models.Organization(**data)
    db_organization.created_date = datetime.datetime.now()
    db_organization.updated_date = datetime.datetime.now()
    db_organization.save()

    return db_organization


@router.get(
    "/{organization_id}",
    response_model_by_alias=False,
    response_model=OrganizationInResponse,
)
def get_organization(
    organization_id: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        db_organization = models.Organization.objects.get(id=organization_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this organization",
        )
    return db_organization


@router.put(
    "/{organization_id}/update",
    response_model_by_alias=False,
    response_model=OrganizationInResponse,
)
def update_organization(
    organization_id: str,
    organization: OrganizationInCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_organization = models.Organization.objects(id=organization_id).first()
    if not db_organization:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    db_organizations = models.Organization.objects(
        name=organization.name, status="active", id__ne=organization_id
    )
    if db_organizations:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already organization name",
        )
    db_organizations = models.Organization.objects(
        code=organization.code, status="active", id__ne=organization_id
    )
    if db_organizations:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already organization code",
        )

    data = organization.dict()
    db_organization.update(**data)

    db_organization.updated_date = datetime.datetime.now()
    db_organization.save()
    db_organization.reload()
    return db_organization


@router.delete(
    "/{organization_id}/delete",
    response_model_by_alias=False,
    response_model=OrganizationInResponse,
)
def delete_organization(
    organization_id: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        db_organization = models.Organization.objects.get(id=organization_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this organization",
        )
    db_organization.update(status="disactive", updated_date=datetime.datetime.now())
    db_organization.reload()
    db_organization.save()

    divisions = models.Division.objects(organization=db_organization, status="active")
    for division in divisions:
        division.status = "disactive"
        division.save()
    return db_organization


@router.post(
    "/{organization_id}/create_authorized_signatory",
    response_model_by_alias=False,
    response_model=OrganizationInResponse,
)
def create_organization_authorized_signatory(
    organization_id: str,
    authorized_signatory: AuthorizedSignatoryInCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_organization = models.Organization.objects(id=organization_id).first()
    if not db_organization:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not Found this organization.",
        )

    signature = models.AuthorizedSignatory()
    signature.first_name = authorized_signatory.first_name
    signature.last_name = authorized_signatory.last_name
    signature.role = authorized_signatory.role
    signature.instead = authorized_signatory.instead
    db_organization.authorized_signatories.append(signature)
    db_organization.updated_date = datetime.datetime.now()
    db_organization.save()

    return db_organization


@router.delete(
    "/{organization_id}/delete_authorized_signatory/{authorized_signatory_id}",
    response_model_by_alias=False,
    response_model=OrganizationInResponse,
)
def delete_organization_authorized_signatory(
    organization_id: str,
    authorized_signatory_id: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_organization = models.Organization.objects(id=organization_id).first()
    if not db_organization:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not Found this organization.",
        )

    for authorized_signatory in db_organization.authorized_signatories:
        if str(authorized_signatory.uid) == authorized_signatory_id:
            db_organization.authorized_signatories.remove(authorized_signatory)
            break

    db_organization.updated_date = datetime.datetime.now()
    db_organization.save()

    return db_organization


@router.put(
    "/{organization_id}/update_authorized_signatory/{authorized_signatory_id}",
    response_model_by_alias=False,
    response_model=OrganizationInResponse,
)
def update_organization_authorized_signatory(
    organization_id: str,
    authorized_signatory_id: str,
    authorized_signatory: AuthorizedSignatoryInUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_organization = models.Organization.objects(id=organization_id).first()
    if not db_organization:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not Found this organization.",
        )
    authorized_signatory_dict = authorized_signatory.dict()
    set_dict = {
        f"set__authorized_signatories__S__{k}": v
        for k, v in authorized_signatory_dict.items()
        if v is not None
    }
    authorized_signatory = models.Organization.objects(
        id=organization_id, authorized_signatories__uid=authorized_signatory_id
    )
    authorized_signatory.update(**set_dict)
    db_organization.save()
    db_organization.reload()

    return db_organization
