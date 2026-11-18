from enum import StrEnum, auto


class CurrencyEnum(StrEnum):
    USD = auto()
    EUR = auto()
    PLN = auto()


class OperationType(StrEnum):
    INCOME = auto()
    OUTCOME = auto()