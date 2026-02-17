from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# HARD-CODED FALLBACK FOR DEBUGGING
# USING PORT 5432 (Direct) with explicit driver scheme
# Try standard port again but with full driver spec
DATABASE_URL = "postgresql+psycopg2://postgres:Roth%40168Roth@db.qqozemdmfzftyltkoevl.supabase.co:5432/postgres"

# 1. Force check for Vercel System Env Var first
if os.environ.get("DATABASE_URL"):
    DATABASE_URL = os.environ.get("DATABASE_URL")

# Ensure scheme is correct for SQLAlchemy
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
elif DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# 2. Use the URL
SQLALCHEMY_DATABASE_URL = DATABASE_URL
print(f"✅ Using Database URL Scheme: {SQLALCHEMY_DATABASE_URL.split(':')[0]}")

# Check if using SQLite
is_sqlite = "sqlite" in SQLALCHEMY_DATABASE_URL

# Connect args
connect_args = {"check_same_thread": False} if is_sqlite else {
    "connect_timeout": 10, # Fail fast
    "application_name": "we-expense-api"
}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True, # Verify connection before usage
    pool_recycle=300,   # Recycle connections every 5 minutes
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
