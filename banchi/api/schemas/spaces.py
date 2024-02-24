from bson import ObjectId

from pydantic import BaseModel, Field
from beanie import PydanticObjectId
import typing

import datetime

from .system_settings import BaseAuthorizedSignatory

from . import bases
from . import users


class Address(BaseModel):
    address: str | None  # บ้านเลขที่
    building: str | None  # อาคาร
    floor: str | None  # ชั้น
    moo: str | None  # หมู่
    village: str | None  # หมู่บ้าน
    alley: str | None  # ซอย
    road: str | None  # ถนน
    subdistrict: str | None  # ตำบล
    district: str | None  # อำเภอ
    province: str | None  # จังหวัด
    zipcode: str | None  # รหัสไปรษณีย์


class BaseSpace(BaseModel):
    name: str = Field(..., example="Space Name")
    code: str | None = Field(..., example="Space Code")
    tax_id: str | None = Field(..., example="Text ID")


class Space(bases.BaseSchema, BaseSpace):
    owner: users.ReferenceUser
    status: str = Field(
        default="active",
        example="active",
    )


class ReferenceSpace(bases.BaseSchema):
    name: str = Field(..., example="Space Name")


class SpaceList(BaseModel):
    spaces: list[Space]


class CreatedSpace(BaseSpace):
    pass


class UpdatedSpace(CreatedSpace):
    pass


class BaseSpaceRole(BaseModel):
    role: typing.Literal["owner", "member"] = Field(..., choices=["owner", "member"])


class SpaceRole(bases.BaseSchema, BaseSpaceRole):
    added_by: users.ReferenceUser
    updated_by: users.ReferenceUser
    member: users.ReferenceUser
    space: ReferenceSpace

    created_date: datetime.datetime
    updated_date: datetime.datetime

    status: typing.Literal["active", "delete"] = Field(default="active")


class SpaceRoleList(BaseModel):
    space_roles: list[SpaceRole]


class CreatedSpaceRole(BaseSpaceRole):
    member_id: PydanticObjectId


class UpdatedSpaceRole(CreatedSpaceRole):
    pass
