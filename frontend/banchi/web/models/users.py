import datetime

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, attr):
        return self.data[attr]

    # def get_id(self) -> str:
    #     id = self.data.get("id", None)
    #     if not id:
    #         additional_properties = self.data.get("additional_properties")
    #         id = additional_properties.get("id")

    #     return id

    def has_roles(self, role) -> bool:
        roles = self.data.get("roles", [])
        return role in roles

    def get_picture(self) -> str | None:
        return None
