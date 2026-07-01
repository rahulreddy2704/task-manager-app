"""
Database configuration.
Uses SQLite for simplicity - no separate DB server needed to run this locally.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Provides a database session for each request, and closes it afterward."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()