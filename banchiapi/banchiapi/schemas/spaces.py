from bson import ObjectId

from pydantic import BaseModel, Field

from .base import BaseEmbeddedSchema, BaseSchema, PyObjectId
from .system_settings import BaseAuthorizedSignatory


class Address(BaseEmbeddedSchema):
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
    name: str = Field(..., example="ชื่อองค์กร")
    code: str = Field(..., example="รหัสองค์กร")
    tax_id: str | None = Field(..., example="เลขผู้เสียภาษี")
    phone: str | None = Field(..., example="เบอร์โทรศัพท์")
    slogan: str | None = Field(..., example="คำขวัญ")
    address: Address


class SpaceAuthorizedSignatoryInResponse(BaseAuthorizedSignatory):
    uid: PyObjectId | None = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class SpaceInResponse(BaseSchema, BaseSpace):
    authorized_signatories: list[SpaceAuthorizedSignatoryInResponse]


class SpaceInCreate(BaseSpace):
    authorized_signatories: list[SpaceAuthorizedSignatoryInResponse]


class SpaceInUserResponse(BaseSchema):
    name: str = Field(..., example="ชื่อองค์กร")


class ListSpaceInResponse(BaseSchema):
    spaces: list[SpaceInResponse]
    count: int
    current_page: int = 0
    total_page: int = 0
