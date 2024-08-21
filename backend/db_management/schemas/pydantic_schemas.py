"""Pydantic models."""
from datetime import datetime

from pydantic import BaseModel



class User(BaseModel):
    """User class."""

    username : str
    email : str
    password : str
    
class UserResponse(BaseModel):
    """User response class."""

    username : str
    email : str


class Trip(BaseModel):
    """Trip class."""

    dt_created : datetime = datetime.now().strftime("%Y-%m-%d %H:%M")  # noqa: DTZ005
    category : str = None
    distance: float
    total_cost: float
    user_id: int = None