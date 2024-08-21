"""Database models."""
import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Declare the base class for models
Base = declarative_base()

class UserAccount(Base):
    """User account table."""

    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)


class TripList(Base):
    """Trip list table."""

    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=False)
    dt_created = Column(String, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))  # noqa: DTZ005
    category = Column(String, nullable=True)
    distance = Column(Integer)
    total_cost = Column(Integer)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=True,
                     server_default=None)