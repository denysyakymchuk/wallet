from fastapi import HTTPException

from app.schemas import OperationRequest
from app.repository import wallets as wallet_repository


def add_income(operation: OperationRequest):
    if not wallet_repository.is_wallet_exists(operation.wallet_name):
        raise HTTPException(status_code=400, detail=f"Wallet {operation.wallet_name} not found")



    new_balance = wallet_repository.add_income(operation.wallet_name, operation.amount)

    return {
        "message": f"Wallet {operation.wallet_name} income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "new_balance": new_balance,
    }

def add_expense(operation: OperationRequest):
    if not wallet_repository.is_wallet_exists(operation.wallet_name):
        raise HTTPException(status_code=400, detail=f"Wallet {operation.wallet_name} not found")

    balance = wallet_repository.get_balance(operation.wallet_name)
    if balance <= operation.amount:
        return HTTPException(status_code=400, detail=f"No enough balance")

    new_balance = wallet_repository.add_expense(operation.wallet_name, operation.amount)

    return {
        "message": f"Wallet {operation.wallet_name} expensed",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "new_balance": new_balance,
    }