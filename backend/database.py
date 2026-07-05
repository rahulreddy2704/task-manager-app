"""
Database configuration.
Uses SQLite for simplicity - no separate DB server needed to run this locally.
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "tasks.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """Provides a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()