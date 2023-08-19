import datetime

from pydantic import BaseModel, EmailStr, Field

from .base import BaseEmbeddedSchema, BaseSchema


class BaseUser(BaseModel):
    email: str = Field(example="admin@email.local")
    username: str = Field(example="admin")
    first_name: str = Field(example="Firstname")
    last_name: str = Field(example="Lastname")


class User(BaseModel):
    pass


class UserList(BaseModel):
    pass


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


class ChangedPasswordUser(BaseModel):
    current_password: str
    new_password: str
