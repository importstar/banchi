import datetime

from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId


class BaseUser(BaseModel):
    email: str = Field(example="admin@email.local")
    username: str = Field(example="admin")
    first_name: str = Field(example="Firstname")
    last_name: str = Field(example="Lastname")


class User(BaseUser):
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId, alias="_id", example="0"
    )

    last_login_date: datetime.datetime | None = Field(
        example="2023-01-01T00:00:00.000000", default=None
    )


class UserList(BaseModel):
    users: list[User]


class Login(BaseModel):
    email: EmailStr
    password: str


class ChangedPassword(BaseModel):
    current_password: str
    new_password: str


class ResetedPassword(BaseModel):
    email: EmailStr
    citizen_id: str


class RegisteredUser(BaseUser):
    password: str = Field(example="password")


class UpdatedUser(BaseUser):
    roles: list[str]


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    scope: str
    issued_at: datetime.datetime


class TokenData(BaseModel):
    user_id: str | None = None


class ChangedPasswordUser(BaseModel):
    current_password: str
    new_password: str
