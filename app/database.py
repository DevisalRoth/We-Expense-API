from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# 1. Force check for Vercel System Env Var first
# This ensures we ignore any local .env file or default if DATABASE_URL is set in Vercel UI
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # If not in system env, try loading from .env file (local dev)
    from dotenv import load_dotenv
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Fallback to SQLite only if absolutely no Postgres URL found
if not DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./expenses.db"
    print("⚠️ WARNING: Using SQLite database (read-only on Vercel!)")
else:
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
    print(f"✅ Using Database: {SQLALCHEMY_DATABASE_URL.split('@')[1] if '@' in SQLALCHEMY_DATABASE_URL else 'Unknown'}")

# Handle Postgres URL if provided (Supabase/Vercel uses postgres:// but SQLAlchemy needs postgresql://)
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Check if using SQLite
is_sqlite = "sqlite" in SQLALCHEMY_DATABASE_URL

# Connect args for SQLite only
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
