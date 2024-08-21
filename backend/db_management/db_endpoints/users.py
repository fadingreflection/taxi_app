"""User API routes."""
import sys
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm

sys.path.append("C:\\Users\\Anastasiya Fedotova\\Desktop\\DS&ML\\github\\task_manager\\task_manager\\app")  # noqa: E501

from db.database import get_db
from db_management.db.database_models import UserAccount
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db_management.schemas.pydantic_schemas import User, UserResponse
from security.auth import create_jwt_token, hash_pw

router=APIRouter()

@router.post("/create_user", response_model=User)
def create_user(item: User,  db: Session = Depends(get_db)):  # noqa: ANN201, B008
    """Create user."""
    if db.query(UserAccount).filter_by(username=item.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This user already exists")
    hashed_password = hash_pw(item.password)
    new_user = UserAccount(username=item.username, email=item.email, hashed_password=hashed_password)  # noqa: E501
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/get_user", response_model=UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):  # noqa: ANN201, B008
    """Get user."""
    user = db.query(UserAccount).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User not found")
    return user

@router.patch("/change_user_info", response_model=User)
def change_user_info(item: User, db: Session = Depends(get_db)):  # noqa: ANN201, B008
    """Change user info."""
    if not db.query(UserAccount).filter_by(username=item.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User not found")
    user = db.query(UserAccount).filter_by(username = item.username).first()
    user.username = item.username
    user.email = item.email
    user.hashed_password = item.hashed_password
    db.commit()
    return user

@router.delete("/del_user")
def delete_user(item: User, db: Session = Depends(get_db)) -> str:  # noqa: B008
    """Delete user."""
    if not db.query(UserAccount).filter_by(username=item.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User not found")
    user  = db.query(UserAccount).filter_by(username=item.username).first()
    db.delete(user)
    db.commit()
    return f"User {user.username} deleted"

@router.post("/login")
def login_user(user: Annotated[OAuth2PasswordRequestForm, Depends()],
               db: Session = Depends(get_db)) -> str:  # noqa: B008
    """Login."""
    db_user = db.query(UserAccount).filter_by(username=user.username).first()
    if db_user and db_user.hashed_password == hash_pw(user.password):
        token = create_jwt_token({"username": user.username})
        return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )