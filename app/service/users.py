from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repository.users import get_user
from app.repository.users import create_user as create_user_repository
from app.schemas import UserResponse

def create_user(db: Session, login: str) -> UserResponse:
    if get_user(db, login):
        raise HTTPException(status_code=400, detail="User already exists")

    user = create_user_repository(db, login)
    db.commit()
    return UserResponse.model_validate(user)