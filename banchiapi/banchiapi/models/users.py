from banchiapi.schemas.users import BaseUser

from beanie import Document, Indexed


class User(BaseUser, Document):
    class Settings:
        name = "users"


__beanie_models__ = [User]
