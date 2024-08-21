"""Database configs."""
import os

from dotenv import load_dotenv
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from db_management.db.database_models import Base  # noqa: F401

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # Get the database URL from .env

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a scoped session for tests
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))  # noqa: E501

def get_db() -> None:
    """Get database."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base.metadata.create_all(bind=engine) #STUB do it only once or move to special file. base must be imported and bound on engine