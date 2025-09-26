# routes/chat.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from models.health_llm import HealthLLM
from routes.auth import verify_token, oauth2_scheme

router = APIRouter(prefix="/chat", tags=["Chat"])

# Initialize the LLM
llm = HealthLLM()


class ChatRequest(BaseModel):
    message: str
    max_length: int = 200
    temperature: float = 0.7


class ChatResponse(BaseModel):
    response: str


@router.post("/", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest, token: str = Depends(oauth2_scheme)
):
    """
    Endpoint to send a user message to the Health LLM and get a response.
    Requires a valid JWT token.
    """
    # Verify user token
    try:
        user_payload = verify_token(token)
        user_id = user_payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        response_text = llm.generate_response(
            prompt=request.message,
            max_length=request.max_length,
            temperature=request.temperature
        )
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")
