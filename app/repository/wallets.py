BALANCE: dict[str, float] = {}

def is_wallet_exists(wallet_name: str) -> bool:
    return wallet_name in BALANCE

def get_all_wallets() -> dict[str, float]:
    return BALANCE.copy()

def get_balance(wallet_name: str) -> float:
    return BALANCE[wallet_name]

def create_wallet(wallet_name: str, amount: float) -> float:
    BALANCE[wallet_name] = amount
    return BALANCE[wallet_name]

def add_income(wallet_name: str, income: float) -> float:
    BALANCE[wallet_name] += income
    return BALANCE[wallet_name]

def add_expense(wallet_name: str, expense: float) -> float:
    BALANCE[wallet_name] -= expense
    return BALANCE[wallet_name]
