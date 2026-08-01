from enum import Enum


class SummaryTypeEnum(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"

    def __str__(self) -> str:
        return str(self.value)
