from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# HARD-CODED FALLBACK FOR DEBUGGING
# Since Vercel Env Var is not being picked up, we use this directly.
# Ideally, this should be hidden, but we need it to work now.
# USING PORT 6543 (Supavisor Transaction Pooler) instead of 5432 to avoid connection limits/timeouts
DATABASE_URL = "postgresql://postgres:Roth%40168Roth@db.qqozemdmfzftyltkoevl.supabase.co:6543/postgres"

# 1. Force check for Vercel System Env Var first
if os.environ.get("DATABASE_URL"):
    DATABASE_URL = os.environ.get("DATABASE_URL")

# 2. Use the URL
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
