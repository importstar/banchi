from enum import Enum


class UpdatedSpaceRoleRole(str, Enum):
    MEMBER = "member"
    OWNER = "owner"

    def __str__(self) -> str:
        return str(self.value)
