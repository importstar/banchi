from bson import ObjectId

from pydantic import BaseModel, Field
from beanie import PydanticObjectId

from .system_settings import BaseAuthorizedSignatory

from . import bases


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
    # id: PydanticObjectId = Field(
    #     default_factory=PydanticObjectId, alias="_id", example="0"
    # )

    status: str = Field(
        default="active",
        example="active",
    )


class SpaceList(BaseModel):
    spaces: list[Space]


class CreatedSpace(BaseSpace):
    pass
