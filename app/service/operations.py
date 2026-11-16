from fastapi import HTTPException

from app.database import SessionLocal
from app.schemas import OperationRequest
from app.repository import wallets as wallet_repository


def add_income(operation: OperationRequest):
    db = SessionLocal()
    try:
        if not wallet_repository.is_wallet_exists(db, operation.wallet_name):
            raise HTTPException(status_code=400, detail=f"Wallet {operation.wallet_name} not found")

        wallet = wallet_repository.add_income(db, operation.wallet_name, operation.amount)

        return {
            "message": f"Wallet {operation.wallet_name} income added",
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "new_balance": wallet.balance,
        }
    finally:
        db.commit()
        db.close()

def add_expense(operation: OperationRequest):
    db = SessionLocal()
    try:
        if not wallet_repository.is_wallet_exists(db, operation.wallet_name):
            raise HTTPException(status_code=400, detail=f"Wallet {operation.wallet_name} not found")

        wallet = wallet_repository.get_balance(db, operation.wallet_name)
        if wallet.balance <= operation.amount:
            return HTTPException(status_code=400, detail=f"No enough balance")

        wallet = wallet_repository.add_expense(db, operation.wallet_name, operation.amount)

        return {
            "message": f"Wallet {operation.wallet_name} expensed",
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "new_balance": wallet.balance,
        }
    finally:
        db.commit()
        db.close()