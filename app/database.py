from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# Check if running on Vercel
IS_VERCEL = os.getenv("VERCEL") == "1"

if IS_VERCEL:
    # Use /tmp directory for SQLite on Vercel (ephemeral)
    SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/expenses.db"
else:
    # Use local directory for development
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./expenses.db")

# Handle Postgres URL if provided (Vercel uses postgres:// but SQLAlchemy needs postgresql://)
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
