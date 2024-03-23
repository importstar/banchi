from fastapi import APIRouter, Depends, HTTPException, Request, status
from banchi.api import schemas
from banchi.api.core import deps
from banchi.api import models
from loguru import logger


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model_by_alias=False, response_model=schemas.users.User)
def get_me(current_user: models.users.User = Depends(deps.get_current_user)):
    return current_user


@router.get(
    "/me/check_password",
    response_model_by_alias=False,
    response_model=bool,
)
async def get_me_check_password(
    current_user: models.users.User = Depends(deps.get_current_user),
):
    return current_user.is_use_citizen_id_as_password()


@router.get(
    "/{user_id}",
    response_model_by_alias=False,
    response_model=schemas.users.User,
)
async def get(
    user_id: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.users.User:
    try:
        user = models.users.User.objects.get(id=user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found this user",
        )
    return user


@router.get(
    "",
    response_model_by_alias=False,
)
async def get_all(
    first_name: str = "",
    last_name: str = "",
    citizen_id: str = "",
    current_page: int = 1,
    limit: int = 50,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.users.UserList:
    users = models.users.User.find()
    count = 0

    if first_name:
        users = users.find(first_name=first_name)

    if last_name:
        users = users.find(last_name=last_name)

    if citizen_id:
        users = users.find(citizen_id=citizen_id)

    count = await users.count()
    users = users.skip((current_page - 1) * limit).limit(limit)

    if count % limit == 0 and count // limit > 0:
        total_page = count // limit
    else:
        total_page = (count // limit) + 1

    users = await users.to_list()
    return schemas.users.UserList(
        users=list(users),
        count=count,
        current_page=current_page,
        total_page=total_page,
    )


@router.post(
    "/create",
    # response_model=schemas.users.User,
    response_model_by_alias=False,
)
async def create(
    user_register: schemas.users.RegisteredUser,
) -> schemas.users.User:
    user = await models.users.User.find_one(
        models.users.User.username == user_register.username
    )

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is exists.",
        )

    user = models.users.User(**user_register.dict())
    await user.set_password(user_register.password)
    await user.insert()

    return user


@router.put(
    "/{user_id}/change_password",
    response_model=schemas.users.User,
    response_model_by_alias=False,
)
def change_password(
    user_id: str,
    password_update: schemas.users.ChangedPassword,
    current_user: models.users.User = Depends(deps.get_current_user),
):
    try:
        user = models.users.User.objects.get(id=user_id)
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
    response_model=schemas.users.User,
    response_model_by_alias=False,
)
def update(
    request: Request,
    user_id: str,
    user_update: schemas.users.UpdatedUser,
    current_user: models.users.User = Depends(deps.get_current_user),
):
    try:
        user = models.users.User.objects.get(id=user_id)
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
    response_model=schemas.users.User,
    response_model_by_alias=False,
)
def set_status(
    request: Request,
    user_id: str,
    status: str = "active",
    current_user: models.users.User = Depends(deps.get_current_user),
):
    try:
        user = models.users.User.objects.get(id=user_id)
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
    response_model=schemas.users.User,
    response_model_by_alias=False,
)
def set_space(
    request: Request,
    user_id: str,
    space_id: str,
    action: str,
    current_user: models.users.User = Depends(deps.get_current_user),
):
    try:
        user = models.users.User.objects.get(id=user_id)
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
    "/{user_id}/set_role",
    response_model_by_alias=False,
)
def set_role(
    request: Request,
    user_id: str,
    role: str,
    action: str,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.users.User:
    try:
        user = models.users.User.objects.get(id=user_id)
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
