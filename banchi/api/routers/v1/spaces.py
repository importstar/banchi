import datetime
import io
import typing

from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from loguru import logger
import bson

from banchi.api import models
from banchi.api import schemas
from banchi.api.core import deps

from beanie import PydanticObjectId
from beanie.odm.operators.find import comparison
from beanie.operators import Inc, Set


router = APIRouter(prefix="/spaces", tags=["spaces"])


@router.get("")
async def get_all(
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
    spaces: typing.Annotated[
        models.spaces.Space, Depends(deps.get_current_user_spaces)
    ],
) -> schemas.spaces.SpaceList:
    return model_dump(spaces=spaces)


@router.post("")
async def create(
    space: schemas.spaces.CreatedSpace,
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:
    db_space = await models.spaces.Space.find_one(
        models.spaces.Space.name == space.name,
        models.spaces.Space.owner.id == current_user.id,
        models.spaces.Space.status == "active",
    )
    if db_space:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already space name",
        )

    db_space = await models.spaces.Space.find_one(
        models.spaces.Space.code == space.code,
        models.spaces.Space.status == "active",
        models.spaces.Space.owner.id == current_user.id,
    )
    if db_space:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There are already space code",
        )

    data = space.model_dump()
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


@router.get("/{space_id}")
async def get(
    space_id: PydanticObjectId,
    space: typing.Annotated[models.spaces.Space, Depends(deps.get_current_user_space)],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.spaces.Space:
    return space


@router.get("/{space_id}/accounts")
async def get_accounts(
    space_id: PydanticObjectId,
    db_account: typing.Annotated[
        models.accounts.Account, Depends(deps.get_account_by_space)
    ],
    current_user: typing.Annotated[models.users.User, Depends(deps.get_current_user)],
) -> schemas.accounts.Account:
    return db_account


@router.put("/{space_id}")
async def update(
    space_id: PydanticObjectId,
    space: schemas.spaces.UpdatedSpace,
    db_space: typing.Annotated[
        models.spaces.Space, Depends(deps.get_current_user_space)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:
    data = space.model_dump()
    await db_space.update(Set(data))

    db_space.updated_date = datetime.datetime.now()
    db_space.updated_by = current_user
    await db_space.save()

    return db_space


@router.post("/{space_id}/copy")
async def copy(
    space_id: PydanticObjectId,
    space: schemas.spaces.CreatedSpace,
    db_space: typing.Annotated[
        models.spaces.Space, Depends(deps.get_current_user_space)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:

    data = space.model_dump()
    data["owner"] = current_user
    data["updated_by"] = current_user

    new_db_space = models.Space.parse_obj(data)
    await new_db_space.save()

    db_space_role = models.spaces.SpaceRole(
        added_by=current_user,
        updated_by=current_user,
        member=current_user,
        role="owner",
        space=new_db_space,
    )
    await db_space_role.save()

    db_account = await models.Account.find_one(
        models.Account.space.id == db_space.id, fetch_links=True
    )

    if not db_account:
        return new_db_space

    data = db_account.model_dump()
    data.pop("id")

    db_new_account = models.Account.parse_obj(data)
    db_new_account.name = f"{space.name} Account"
    db_new_account.created_date = datetime.datetime.now()
    db_new_account.updated_date = datetime.datetime.now()
    db_new_account.creator = current_user
    db_new_account.space = new_db_space
    await db_new_account.save()

    db_account_books = await models.AccountBook.find(
        models.AccountBook.account.id == db_account.id,
        models.AccountBook.parent == None,
        fetch_links=True,
    ).to_list()

    async def copy_account_books(
        db_account, db_new_account, db_account_book, db_new_account_book
    ):

        db_children_account_books = await models.AccountBook.find(
            models.AccountBook.account.id == db_account.id,
            models.AccountBook.parent.id == db_account_book.id,
            fetch_links=True,
        ).to_list()
        for db_children_account_book in db_children_account_books:

            data = db_children_account_book.model_dump()
            data.pop("id")
            db_new_children_account_book = models.AccountBook.parse_obj(data)
            db_new_children_account_book.created_date = datetime.datetime.now()
            db_new_children_account_book.updated_date = datetime.datetime.now()
            db_new_children_account_book.creator = current_user
            db_new_children_account_book.parent = db_new_account_book
            db_new_children_account_book.account = db_new_account

            await db_new_children_account_book.save()
            await copy_account_books(
                db_account,
                db_new_account,
                db_children_account_book,
                db_new_children_account_book,
            )

    for db_account_book in db_account_books:
        data = db_account_book.model_dump()
        data.pop("id")
        db_new_account_book = models.AccountBook.parse_obj(data)
        db_new_account_book.created_date = datetime.datetime.now()
        db_new_account_book.updated_date = datetime.datetime.now()
        db_new_account_book.creator = current_user
        db_new_account_book.account = db_new_account
        await db_new_account_book.save()

        await copy_account_books(
            db_account, db_new_account, db_account_book, db_new_account_book
        )

    return new_db_space


@router.delete("/{space_id}")
async def delete(
    space_id: PydanticObjectId,
    db_space: typing.Annotated[
        models.spaces.Space, Depends(deps.get_current_user_space)
    ],
    current_user: models.users.User = Depends(deps.get_current_user),
) -> schemas.spaces.Space:
    db_space.status = "disactive"
    db_space.updated_date = datetime.datetime.now()
    db_space.updated_by = current_user
    await db_space.save()

    return db_space
