# backend/database.py
import os
from supabase import create_client, Client
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import settings

supabase: Client | None = None
engine = None
async_session: sessionmaker | None = None


def init_supabase() -> Client:
    """
    Initialize Supabase client using config values.
    """
    global supabase
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("Supabase URL or Key is missing. Check your .env file.")

    supabase = create_client(str(settings.SUPABASE_URL), settings.SUPABASE_KEY)
    return supabase


def init_sqlalchemy():
    """
    Initialize SQLAlchemy async engine if DATABASE_URL is set.
    This is optional — useful if you use relational tables in Supabase.
    """
    global engine, async_session
    if not settings.DATABASE_URL:
        return None

    engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session


# Run at startup
try:
    supabase = init_supabase()
    init_sqlalchemy()
    print("✅ Database connections initialized")
except Exception as e:
    print(f"⚠️ Database init error: {e}")
