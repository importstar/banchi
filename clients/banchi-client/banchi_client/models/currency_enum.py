from enum import Enum


class CurrencyEnum(str, Enum):
    THB = "THB"
    USD = "USD"

    def __str__(self) -> str:
        return str(self.value)
