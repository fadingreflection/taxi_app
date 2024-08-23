"""Database models."""
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Declare the base class for models
Base = declarative_base()

class UserAccount(Base):
    """User account table."""

    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    trips = relationship("TripList", back_populates="users",  cascade="all, delete-orphan") # one to many relationship. Deletes child without parent 


class TripList(Base):
    """Trip list table."""

    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dt_created = Column(String, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))  # noqa: DTZ005
    category = Column(String, nullable=True)
    distance = Column(Integer)
    total_cost = Column(Integer)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=True,
                     server_default=None)
    users = relationship("UserAccount", back_populates="trips")