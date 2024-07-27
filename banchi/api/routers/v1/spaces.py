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
    return dict(spaces=spaces)


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
    data = space.dict()
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
    # data = space.dict()
    # await db_space.update(Set(data))

    # db_space.updated_date = datetime.datetime.now()
    # db_space.updated_by = current_user
    # await db_space.save()

    data = space.dict()
    data["owner"] = current_user
    data["updated_by"] = current_user
    data["code"] = f"{db_space.code}-copy"
    data["name"] = f"{db_space.name}-copy"

    new_db_space = models.spaces.Space.parse_obj(data)
    await new_db_space.save()

    db_space_role = models.spaces.SpaceRole(
        added_by=current_user,
        updated_by=current_user,
        member=current_user,
        role="owner",
        space=new_db_space,
    )
    await db_space_role.save()

    db_account = await models.accounts.Account.find_one(space == db_space)

    if not db_account:
        return new_db_space

    new_db_account = models.accounts.Account(db_account.dict())
    new_db_account.created_date = datetime.datetime.now()
    new_db_account.updated_date = datetime.datetime.now()
    new_db_account.owner = current_user
    await new_db_account.save()

    db_account_books = await models.account_books.AccountBook.find(
        account == db_account, parrent=None
    )

    async def copy_account_books(db_account, db_account_book, db_new_account_book):

        db_children_account_books = await models.account_books.AccountBook.find(
            account == db_account, parrent == db_account_book
        )
        for db_children_account_book in db_children_account_books:
            new_children_account_book = models.account_books.AccountBook(
                db_account_book.dict()
            )
            new_children_account_book.created_date = datetime.datetime.now()
            new_children_account_book.updated_date = datetime.datetime.now()
            new_children_account_book.owner = current_user
            await new_children_account_book.save()
            await copy_account_books(
                db_account, db_children_account_book, new_children_account_book
            )

    for db_account_book in db_account_books:
        new_account_book = models.account_books.AccountBook(db_account_book.dict())
        new_account_book.created_date = datetime.datetime.now()
        new_account_book.updated_date = datetime.datetime.now()
        new_account_book.owner = current_user
        await new_account_book.save()

        await copy_account_books(db_account, db_account_book, db_new_account_book)

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
