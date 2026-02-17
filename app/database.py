from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Base class for models
Base = declarative_base()

# Global variables
engine = None
SessionLocal = None

def get_database_url():
    # HARD-CODED FALLBACK FOR DEBUGGING
    # USING PORT 5432 (Direct) with explicit driver scheme
    url = "postgresql+psycopg2://postgres:Roth%40168Roth@db.qqozemdmfzftyltkoevl.supabase.co:5432/postgres"
    
    # 1. Force check for Vercel System Env Var first
    if os.environ.get("DATABASE_URL"):
        url = os.environ.get("DATABASE_URL")
    
    # Ensure scheme is correct for SQLAlchemy
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url and url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
    return url

def init_db():
    global engine, SessionLocal
    
    url = get_database_url()
    print(f"✅ Initializing Database with URL Scheme: {url.split(':')[0]}")
    
    is_sqlite = "sqlite" in url
    
    connect_args = {"check_same_thread": False} if is_sqlite else {
        "connect_timeout": 10,
        "application_name": "we-expense-api"
    }
    
    try:
        engine = create_engine(
            url, 
            connect_args=connect_args,
            pool_pre_ping=True, 
            pool_recycle=300,
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return True
    except Exception as e:
        print(f"❌ Failed to create engine: {e}")
        return False

# Initialize immediately (but inside try-catch block in main.py)
init_db()
