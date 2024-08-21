"""Security block."""
import hashlib  # noqa: INP001
import os
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from db_management.db.database import get_db
from db_management.db.database_models import UserAccount

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXP_TIME = timedelta(minutes=30)    # время жизни токена

def create_jwt_token(data: dict) -> str:
    """Create token."""
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def hash_pw(password: str):
    """Hash password."""
    hashed = hashlib.md5((password + os.getenv("SALT")).encode())  # noqa: S324
    return hashed.hexdigest()


def get_jwt_token(username: str) -> dict:
    """Get jwt token."""
    try:
        return {"access_token": create_jwt_token({
            "sub": username,
            "exp": datetime.utcnow() + EXP_TIME})}  # noqa: DTZ003
    except jwt.ExpiredSignatureError:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_from_token(token=Depends(oauth2_scheme)) -> str:  # noqa: ANN001, B008
    """Get user from token."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")


def get_user(current_user: str, db: Session = Depends(get_db)):  # noqa: ANN201
    """Get user."""
    from_db = db.execute(select(UserAccount).where(UserAccount.username == current_user))
    return from_db.scalars().all()[0]