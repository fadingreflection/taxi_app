"""User API routes."""

from __future__ import annotations

from typing import TYPE_CHECKING

from db_management.db.database import get_db
from db_management.db.database_models import UserAccount
from db_management.schemas.pydantic_schemas import User, UserResponse
from db_management.security.auth import create_jwt_token, hash_pw
from fastapi import APIRouter, Depends, HTTPException, status

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create_user", response_model=User)
def create_user(item: User, db: Session = Depends(get_db)):  # noqa: ANN201, B008
    """Create user."""
    if db.query(UserAccount).filter_by(username=item.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This user already exists",
        )
    hashed_password = hash_pw(item.password)
    new_user = UserAccount(
        username=item.username, email=item.email, hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return item


@router.get("/get_user", response_model=UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):  # noqa: ANN201, B008
    """Get user."""
    user = db.query(UserAccount).filter_by(username=username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found",
        )
    return user


@router.patch("/change_user_info", response_model=User)
def change_user_info(item: User, db: Session = Depends(get_db)):  # noqa: ANN201, B008
    """Change user info."""
    if not db.query(UserAccount).filter_by(username=item.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found",
        )
    user = db.query(UserAccount).filter_by(username=item.username).first()
    user.email = item.email
    user.hashed_password = hash_pw(item.password)
    db.commit()
    return item


@router.delete("/del_user")
def delete_user(item: User, db: Session = Depends(get_db)) -> str:  # noqa: B008
    """Delete user."""
    if not db.query(UserAccount).filter_by(username=item.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found",
        )
    user = db.query(UserAccount).filter_by(username=item.username).first()
    db.delete(user)
    db.commit()
    return f"User {user.username} deleted"


@router.get("/login")
def login_user(
    username: str, password: str, db: Session = Depends(get_db),  # noqa: B008
) -> dict | str:
    """Login."""
    db_user = db.query(UserAccount).filter_by(username=username).first()
    if db_user and db_user.hashed_password == hash_pw(password):
        token = create_jwt_token({"username": username})
        status = 0
        return {"token": token, "status": status}
    return "Authorization error: try again or register."
