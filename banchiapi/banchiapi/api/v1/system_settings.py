import datetime
import io

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Response, Request
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST
from starlette.responses import StreamingResponse
from loguru import logger
from banchaiapi import models
from banchaiapi.core import deps
from banchaiapi.schemas.system_settings import (
    SystemSettingInCreate,
    SystemSettingInResponse,
)

router = APIRouter(prefix="/system_settings", tags=["system_settings"])


@router.post(
    "/create",
    response_model_by_alias=False,
    response_model=SystemSettingInResponse,
)
def create_system_setting(
    request: Request,
    system_setting: SystemSettingInCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_system_setting = models.SystemSetting.objects().first()
    if db_system_setting:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="There are already setting in system",
        )
    data = system_setting.dict()
    db_system_setting = models.SystemSetting(**data)
    request_log = deps.create_logs(
        action="create", request=request, current_user=current_user
    )
    db_system_setting.request_logs.append(request_log)
    db_system_setting.created_date = datetime.datetime.now()
    db_system_setting.updated_date = datetime.datetime.now()
    db_system_setting.save()

    return db_system_setting


@router.get(
    "",
    response_model_by_alias=False,
    response_model=SystemSettingInResponse,
)
def get_system_setting():
    system_setting = models.SystemSetting.objects().first()
    if not system_setting:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    return system_setting


@router.put(
    "/{system_setting_id}/update",
    response_model_by_alias=False,
    response_model=SystemSettingInResponse,
)
def update_system_setting(
    request: Request,
    system_setting_id: str,
    system_setting: SystemSettingInCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_system_setting = models.SystemSetting.objects(id=system_setting_id).first()
    if not db_system_setting:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    system_setting_dict = system_setting.dict()
    set_dict = {f"set__{k}": v for k, v in system_setting_dict.items() if v is not None}
    request_log = deps.create_logs(
        action="update", request=request, current_user=current_user
    )
    db_system_setting.request_logs.append(request_log)
    db_system_setting.update(**set_dict)
    db_system_setting.updated_date = datetime.datetime.now()
    db_system_setting.save()
    db_system_setting.reload()
    return db_system_setting


@router.put(
    "/{system_setting_id}/upload_logo",
    response_model_by_alias=False,
    response_model=SystemSettingInResponse,
)
def upload_logo_system_setting(
    system_setting_id: str,
    files: UploadFile | None = None,
    # request: Request = None,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_system_setting = models.SystemSetting.objects(id=system_setting_id).first()
    if not db_system_setting:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    # if not files or files.content_type != "image/jpeg" or files.content_type != "image/png":
    #     raise HTTPException(
    #         status_code=HTTP_400_BAD_REQUEST,
    #         detail="No file uploaded or file type was wrong.",
    #     )
    if db_system_setting.logo:
        db_system_setting.logo.replace(
            files.file, filename=files.filename, content_type=files.content_type
        )
    else:
        db_system_setting.logo.put(
            files.file, filename=files.filename, content_type=files.content_type
        )
    db_system_setting.updated_date = datetime.datetime.now()
    db_system_setting.save()
    db_system_setting.reload()
    return db_system_setting


@router.get(
    "/{system_setting_id}/get_logo",
    response_model_by_alias=False,
    response_class=Response,
)
def get_logo_system_setting(
    system_setting_id: str,
):
    db_system_setting = models.SystemSetting.objects(id=system_setting_id).first()
    if not db_system_setting:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    if not db_system_setting.logo:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found logo",
        )

    return StreamingResponse(
        io.BytesIO(db_system_setting.logo.read()),
        media_type=db_system_setting.logo.content_type,
    )


@router.delete(
    "/{system_setting_id}/delete_logo",
    response_model_by_alias=False,
    response_model=SystemSettingInResponse,
)
def delete_logo_system_setting(
    system_setting_id: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    db_system_setting = models.SystemSetting.objects(id=system_setting_id).first()
    if not db_system_setting:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this system setting",
        )
    if not db_system_setting.logo:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found logo",
        )

    db_system_setting.logo.delete()
    db_system_setting.logo = None
    db_system_setting.updated_date = datetime.datetime.now()
    db_system_setting.save()
    db_system_setting.reload()
    return db_system_setting
