from decimal import Decimal

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Wallet, User


def is_wallet_exists(db: Session, user_id: int, wallet_name: str) -> bool:
    return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id==user_id).first() is not None


def get_all_wallets(db: Session, user_id: int) -> list[Wallet]:
    return db.query(Wallet).filter(User.id == user_id, Wallet.user_id==user_id).all()

def get_balance(db: Session, user_id: int,  wallet_name: str) -> Wallet:
    return db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id==user_id).scalar()


def create_wallet(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = Wallet(name=wallet_name, balance=amount, user_id=user_id)
    db.add(wallet)
    db.flush(wallet)
    return wallet

def add_income(db: Session, user_id: int, wallet_name: str, income: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id==user_id).scalar()
    wallet.balance += income
    return wallet


def add_expense(db: Session, user_id: int, wallet_name: str, expense: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name, Wallet.user_id==user_id).scalar()
    wallet.balance -= expense
    return wallet

