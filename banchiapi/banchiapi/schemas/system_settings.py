from pydantic import BaseModel, Field

from .base import BaseSchema, BaseEmbeddedSchema


class BaseSystemSetting(BaseModel):
    title_names: list[str]
    banks: list[str]
    bill_expired: int | None
    year: str | None  # ปีงบประมาณ
    vat: float | None


class SystemSettingInResponse(BaseSchema, BaseSystemSetting):
    pass


class SystemSettingInCreate(BaseSystemSetting):
    pass


class BaseAuthorizedSignatory(BaseModel):
    first_name: str = Field(..., example="ชื่อ")
    last_name: str = Field(..., example="นามสกุล")
    role: str = Field(..., example="ตำแหน่ง")
    instead: str = Field(..., example="แทน")


class AuthorizedSignatoryInCreate(BaseAuthorizedSignatory):
    pass


class AuthorizedSignatoryInUpdate(BaseAuthorizedSignatory):
    pass
