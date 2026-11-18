from fastapi import HTTPException
from parso import tree
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.repository import wallets as wallet_repository
from app.schemas import CreateWalletRequest, WalletResponse


def get_wallet(db: Session, current_user: User, wallet_name: str | None = None):
    if wallet_name is None:
        wallets =  wallet_repository.get_all_wallets(db, current_user)
        return {"total_balance": sum([w.amount for w in wallets]), "wallets": wallets}

    if not wallet_repository.is_wallet_exists(db, current_user.id, wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet {wallet_name} not found")

    wallet = wallet_repository.get_balance(db, current_user.id, wallet_name)

    return {"wallet": wallet.name, 'balance': wallet.balance}


def create_wallet(db: Session, current_user: User, wallet: CreateWalletRequest) -> WalletResponse:
    if wallet_repository.is_wallet_exists(db, current_user.id, wallet.name):
        raise HTTPException(status_code=400, detail=f"Wallet {wallet.name} already exists")

    wallet = wallet_repository.create_wallet(db, current_user.id, wallet.name, wallet.initial_balance, wallet.currency)
    db.commit()

    return WalletResponse.model_validate(wallet)
