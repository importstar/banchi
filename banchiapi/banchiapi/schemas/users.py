import datetime

from pydantic import BaseModel, EmailStr, Field

from .base import BaseEmbeddedSchema, BaseSchema
from .divisions import DivisionInUserResponse
from .organizations import OrganizationInUserResponse


class UserAddress(BaseEmbeddedSchema):
    address: str | None  # บ้านเลขที่
    building: str| None  # อาคาร
    floor: str| None  # ชั้น
    moo: str| None  # หมู่
    village: str| None  # หมู่บ้าน
    alley: str| None  # ซอย
    road: str| None  # ถนน
    subdistrict: str| None  # ตำบล
    district: str| None  # อำเภอ
    province: str| None  # จังหวัด
    zipcode: str| None  # รหัสไปรษณีย์


class BaseUser(BaseModel):
    email: str| None
    username: str| None
    title_name: str| None
    first_name: str| None
    last_name: str| None
    phone: str| None
    address: UserAddress
    citizen_id: str| None
    birthday: datetime.datetime | None 
    employee_id: str| None


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str


class UserResetPassword(BaseModel):
    email: EmailStr
    citizen_id: str


class UserInRegister(BaseUser):
    password: str


class UserInUpdate(BaseUser):
    roles: list[str]


class TokenInResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    scope: str
    issued_at: datetime.datetime


class UserInResponse(BaseSchema, BaseUser):
    username: str
    roles: list[str]
    division: DivisionInUserResponse | None = Field(None, alias="DivisionInUserResponse")
    organization: OrganizationInUserResponse | None = Field(None, alias="OrganizationInUserResponse")
    last_login_date: datetime.datetime 
    employee_id: str | None


class ListUserInResponse(BaseSchema):
    users: list[UserInResponse]
    count: int
    current_page: int = 0
    total_page: int = 0

class UserInAutoCreate(BaseUser):
    pass


class UserDependInResponse(BaseSchema, UserInAutoCreate):
    pass


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str
