# backend/utils/supabase_utils.py
from supabase import create_client, Client
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

# -------------------------
# Initialize Supabase client
# -------------------------
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


# -------------------------
# Auth Helpers
# -------------------------
def get_user_by_email(email: str):
    """Fetch user details by email"""
    try:
        response = supabase.table("users").select("*").eq("email", email).single().execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching user {email}: {e}")
        return None


def insert_user(user_data: dict):
    """Insert a new user into users table"""
    try:
        response = supabase.table("users").insert(user_data).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error inserting user {user_data}: {e}")
        return None


# -------------------------
# Analytics Helpers
# -------------------------
def save_health_score(user_id: str, score: float):
    """Save computed health score"""
    try:
        response = supabase.table("health_scores").insert(
            {"user_id": user_id, "score": score}
        ).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error saving health score for {user_id}: {e}")
        return None


def fetch_health_scores(user_id: str):
    """Fetch all health scores for a user"""
    try:
        response = supabase.table("health_scores").select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching health scores for {user_id}: {e}")
        return []


# -------------------------
# Document Helpers
# -------------------------
def save_document(user_id: str, filename: str, content: str):
    """Save uploaded or generated medical documents"""
    try:
        response = supabase.table("documents").insert(
            {"user_id": user_id, "filename": filename, "content": content}
        ).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error saving document for {user_id}: {e}")
        return None


def fetch_documents(user_id: str):
    """Fetch all documents for a user"""
    try:
        response = supabase.table("documents").select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching documents for {user_id}: {e}")
        return []
