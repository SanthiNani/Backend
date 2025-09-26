# backend/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import jwt
from pydantic import BaseModel
from config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# -------------------------
# Pydantic Models
# -------------------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserCredentials(BaseModel):
    username: str
    password: str

# -------------------------
# JWT Functions
# -------------------------
def create_access_token(data: dict, expires_delta: int = settings.JWT_EXPIRY_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -------------------------
# Routes
# -------------------------
@router.post("/login", response_model=TokenResponse)
def login(credentials: UserCredentials):
    """
    Dummy login route. Replace with real user authentication.
    """
    # For demonstration, accept any username/password
    user_data = {"sub": credentials.username}
    access_token = create_access_token(user_data)
    return {"access_token": access_token, "token_type": "bearer"}
