from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from banchiapi.schemas.users import (
    UserInResponse,
    UserInRegister,
    UserChangePassword,
    UserInUpdate,
    ListUserInResponse,
)
from banchiapi.core import deps
from banchiapi import models
from loguru import logger


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model_by_alias=False, response_model=UserInResponse)
def get_me(current_user: models.User = Depends(deps.get_current_user)):
    return current_user


@router.get(
    "/me/check_password",
    response_model_by_alias=False,
    response_model=bool,
)
def get_me_check_password(
    current_user: models.User = Depends(deps.get_current_user),
):
    return current_user.is_use_citizen_id_as_password()


@router.get(
    "/{user_id}",
    response_model_by_alias=False,
    response_model=UserInResponse,
)
def get_user(
    user_id: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        user = models.User.objects.get(id=user_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    return user


@router.get(
    "/",
    response_model_by_alias=False,
    response_model=ListUserInResponse,
)
def get_users(
    first_name: str = "",
    last_name: str = "",
    citizen_id: str = "",
    current_page: int = 1,
    limit: int = 50,
    current_user: models.User = Depends(deps.get_current_user),
):
    users = []
    count = 0
    is_search = False

    if first_name:
        if users:
            users = users.filter(first_name__contains=first_name)
        elif not is_search:
            users = models.User.objects(first_name__contains=first_name).order_by(
                "-created_date"
            )
        is_search = True

    if last_name:
        if users:
            users = users.filter(last_name__contains=last_name)
        elif not is_search:
            users = models.User.objects(last_name__contains=last_name).order_by(
                "-created_date"
            )
        is_search = True

    if citizen_id:
        if users:
            users = users.filter(citizen_id__contains=citizen_id)
        elif not is_search:
            users = models.User.objects(citizen_id__contains=citizen_id).order_by(
                "-created_date"
            )
        is_search = True

    if users:
        count = users.count()
        users = users.skip((current_page - 1) * limit).limit(limit)

    elif not is_search:
        count = models.User.objects().count()
        users = (
            models.User.objects()
            .order_by("-created_date")
            .skip((current_page - 1) * limit)
            .limit(limit)
        )

    if count % limit == 0 and count // limit > 0:
        total_page = count // limit
    else:
        total_page = (count // limit) + 1

    return ListUserInResponse(
        users=list(users),
        count=count,
        current_page=current_page,
        total_page=total_page,
    )


@router.post(
    "/create",
    response_model=UserInResponse,
    response_model_by_alias=False,
    name="user:create",
)
def create(user_register: UserInRegister):
    user = models.User.objects(username=user_register.username).first()
    if user:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="This username is exists.",
        )
    user = models.User(**user_register.dict())
    user.set_password(user_register.password)
    user.save()
    return user


@router.put(
    "/{user_id}/change_password",
    response_model=UserInResponse,
    response_model_by_alias=False,
    name="user:change_password",
)
def change_password(
    user_id: str,
    password_update: UserChangePassword,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        user = models.User.objects.get(id=user_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    if not user.verify_password(password_update.current_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    user.set_password(password_update.new_password)
    user.save()
    return user


@router.put(
    "/{user_id}/update",
    response_model=UserInResponse,
    response_model_by_alias=False,
    name="user:update",
)
def update(
    request: Request,
    user_id: str,
    user_update: UserInUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        user = models.User.objects.get(id=user_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )

    set_dict = {f"set__{k}": v for k, v in user_update.dict().items() if v is not None}

    user.update(**set_dict)

    user.reload()
    # request_log = deps.create_logs(
    #     action="update", request=request, current_user=current_user
    # )
    # user.request_logs.append(request_log)
    if user.citizen_id:
        user.citizen_id = user.citizen_id.replace("-", "")
    user.save()
    return user


@router.put(
    "/{user_id}/set_status",
    response_model=UserInResponse,
    response_model_by_alias=False,
    name="user:set_status",
)
def set_status(
    request: Request,
    user_id: str,
    status: str = "active",
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        user = models.User.objects.get(id=user_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    user.update(status=status)
    user.reload()
    # request_log = deps.create_logs(
    #     action="update", request=request, current_user=current_user
    # )
    # user.request_logs.append(request_log)
    user.save()
    return user


@router.put(
    "/{user_id}/set_space",
    response_model=UserInResponse,
    response_model_by_alias=False,
    name="user:set_space",
)
def set_space(
    request: Request,
    user_id: str,
    space_id: str,
    action: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        user = models.User.objects.get(id=user_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    if action == "add":
        try:
            space = models.Space.objects.get(id=space_id)
        except Exception:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Not found this space",
            )
        user.update(space=space)
    elif action == "remove":
        user.update(division=None)
        user.update(space=None)

    user.reload()
    # request_log = deps.create_logs(
    #     action="update", request=request, current_user=current_user
    # )
    # user.request_logs.append(request_log)
    user.save()
    return user


@router.put(
    "/{user_id}/set_division",
    response_model=UserInResponse,
    response_model_by_alias=False,
    name="user:set_division",
)
def set_division(
    request: Request,
    user_id: str,
    division_id: str,
    action: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        user = models.User.objects.get(id=user_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    if action == "add":
        try:
            division = models.Division.objects.get(id=division_id)
        except Exception:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Not found this division",
            )
        user.update(division=division)
    elif action == "remove":
        user.update(division=None)

    user.reload()
    # request_log = deps.create_logs(
    #     action="update", request=request, current_user=current_user
    # )
    # user.request_logs.append(request_log)
    user.save()
    return user


@router.put(
    "/{user_id}/set_role",
    response_model=UserInResponse,
    response_model_by_alias=False,
    name="user:set_role",
)
def set_role(
    request: Request,
    user_id: str,
    role: str,
    action: str,
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        user = models.User.objects.get(id=user_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    if action == "add":
        user.roles.append(role)
    elif action == "remove":
        user.roles.remove(role)
    user.save()
    # request_log = deps.create_logs(
    #     action="update", request=request, current_user=current_user
    # )
    # user.request_logs.append(request_log)
    return user
