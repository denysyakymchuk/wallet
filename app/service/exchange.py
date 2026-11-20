from decimal import Decimal
from typing import Tuple, Dict
from app.enum import CurrencyEnum

FALLBACK_RATES: Dict[Tuple[str, str], Decimal] = {
    (CurrencyEnum.PLN, CurrencyEnum.USD): Decimal(str(95.0)),
    (CurrencyEnum.PLN, CurrencyEnum.EUR): Decimal(str(95.0)),
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(95.0)),
    (CurrencyEnum.USD, CurrencyEnum.PLN): Decimal(str(95.0)),
    (CurrencyEnum.EUR, CurrencyEnum.PLN): Decimal(str(95.0)),
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(95.0)),
}


def get_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
    return FALLBACK_RATES.get((base, target), Decimal(1))