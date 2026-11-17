from fastapi import HTTPException
from parso import tree
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.repository import wallets as wallet_repository
from app.schemas import CreateWalletRequest


def get_wallet(db: Session, current_user: User, wallet_name: str | None = None):
    if wallet_name is None:
        wallets =  wallet_repository.get_all_wallets(db, user_id)
        return {"total_balance": sum([w.amount for w in wallets]), "wallets": wallets}

    if not wallet_repository.is_wallet_exists(db, wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet {wallet_name} not found")

    wallet = wallet_repository.get_balance(db, wallet_name)

    return {"wallet": wallet.name, 'balance': wallet.balance}


def create_wallet(db: Session, current_user: User, wallet: CreateWalletRequest):
    if wallet_repository.is_wallet_exists(db, wallet.name):
        raise HTTPException(status_code=400, detail=f"Wallet {wallet.name} already exists")

    wallet = wallet_repository.create_wallet(db, wallet.name, wallet.initial_balance)
    db.commit()

    return {
        "message": f"Wallet {wallet.name} created",
        "wallet": wallet.name,
        "balance": wallet.balance,
    }
