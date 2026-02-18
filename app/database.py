from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base class for models
Base = declarative_base()

# Global variables
engine = None
SessionLocal = None
db_init_error = None

def get_database_url():
    # HARD-CODED FALLBACK FOR DEBUGGING
    # USING PORT 6543 (Transaction Pooler) to avoid IPv6 issues on Vercel
    url = "postgresql+psycopg2://postgres:Roth%40168Roth@db.qqozemdmfzftyltkoevl.supabase.co:6543/postgres?sslmode=require"
    
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
    global engine, SessionLocal, db_init_error
    
    url = get_database_url()
    # Mask password for logs
    safe_url = url
    if "@" in url:
        try:
            # simple masking
            part1 = url.split("@")[0]
            part2 = url.split("@")[1]
            safe_url = f"{part1.split(':')[0]}:***@{part2}"
        except:
            pass
            
    print(f"✅ Initializing Database with URL: {safe_url}")
    
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
        db_init_error = None
        return True
    except Exception as e:
        db_init_error = str(e)
        print(f"❌ Failed to create engine: {e}")
        return False

# Initialize immediately (but inside try-catch block in main.py)
init_db()
