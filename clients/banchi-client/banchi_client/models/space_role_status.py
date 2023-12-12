from enum import Enum


class SpaceRoleStatus(str, Enum):
    ACTIVE = "active"
    DELETE = "delete"

    def __str__(self) -> str:
        return str(self.value)
