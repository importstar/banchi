from enum import IntEnum


class SmallestFractionEnum(IntEnum):
    VALUE_1 = 1
    VALUE_10 = 10
    VALUE_100 = 100
    VALUE_1000 = 1000
    VALUE_10000 = 10000
    VALUE_100000 = 100000
    VALUE_1000000 = 1000000

    def __str__(self) -> str:
        return str(self.value)
