from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.enum import OperationType
from app.models import User
from app.schemas import OperationRequest, OperationResponse
from app.repository import wallets as wallet_repository
from app.repository import operations as operations_repository


def add_income(db: Session, current_user: User, operation: OperationRequest) -> OperationResponse:
    if not wallet_repository.is_wallet_exists(db, current_user.id, operation.wallet_name):
        raise HTTPException(status_code=400, detail=f"Wallet {operation.wallet_name} not found")

    wallet = wallet_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)

    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type=OperationType.INCOME,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description,
    )

    db.commit()
    return OperationResponse.model_validate(operation)

def add_expense(db: Session, current_user: User, operation: OperationRequest) -> OperationResponse:
    if not wallet_repository.is_wallet_exists(db, current_user.id, operation.wallet_name):
        raise HTTPException(status_code=400, detail=f"Wallet {operation.wallet_name} not found")

    wallet = wallet_repository.get_balance(db, current_user.id, operation.wallet_name)
    if wallet.balance <= operation.amount:
        return HTTPException(status_code=400, detail=f"No enough balance")

    wallet = wallet_repository.add_expense(db, current_user.id, operation.wallet_name, operation.amount)

    operation = operations_repository.create_operation(
        db=db,
        wallet_id=wallet.id,
        type=OperationType.OUTCOME,
        amount=operation.amount,
        currency=wallet.currency,
        category=operation.description,
    )

    db.commit()
    return OperationResponse.model_validate(operation)


def get_operational_list(db: Session,
                         current_user: User,
                         wallet_id: int,
                         date_from: datetime | None = None,
                         date_to: datetime | None = None,
                         ) ->list[OperationResponse]:
    if wallet_id:
        wallet = wallet_repository.get_balance(db, current_user.id, wallet_id)
        if not wallet:
            raise HTTPException(status_code=404, detail=f"Wallet {wallet_id} not found")

        wallets_ids = [wallet.id]

    else:
        wallets = wallet_repository.get_all_wallets(db, current_user.id)
        wallets_ids = [w.id for w in wallets]

    operations = operations_repository.get_operation_list(
        db,
        wallets_ids,
        date_from,
        date_to
    )

    result = []

    for operation in operations:
        result.append(OperationResponse.model_validate(operation))
    return result