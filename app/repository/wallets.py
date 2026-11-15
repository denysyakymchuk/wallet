from decimal import Decimal

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Wallet


def is_wallet_exists(db: Session, wallet_name: str) -> bool:
    return db.query(Wallet).filter(Wallet.name == wallet_name).first() is not None


def get_all_wallets(db: Session, ) -> list[Wallet]:
    return db.query(Wallet).all()

def get_balance(db: Session, wallet_name: str) -> Wallet:
    return db.query(Wallet).filter(Wallet.name == wallet_name).scalar()


def create_wallet(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = Wallet(name=wallet_name, balance=amount)
    db.add(wallet)
    db.flush(wallet)
    return wallet

def add_income(db: Session, wallet_name: str, income: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).scalar()
    wallet.balance += income
    return wallet



def add_expense(db: Session, wallet_name: str, expense: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).scalar()
    wallet.balance -= expense
    return wallet

