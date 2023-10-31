from enum import Enum


class AccountTypeEnum(str, Enum):
    ASSET = "asset"
    BANK = "bank"
    CASH = "cash"
    CREDIT_CARD = "credit card"
    LIABILITY = "liability"
    MULTUAL_FUND = "multual fund"
    STOCK = "stock"

    def __str__(self) -> str:
        return str(self.value)
