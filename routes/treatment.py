# backend/routes/treatment.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from routes.auth import verify_token, oauth2_scheme
from models.health_llm import HealthLLM

router = APIRouter(prefix="/treatment", tags=["Treatment"])

# Initialize LLM
llm = HealthLLM()

# -------------------------
# Pydantic Models
# -------------------------
class TreatmentRequest(BaseModel):
    disease_name: str
    patient_age: int = None
    patient_conditions: str = None  # e.g., "diabetic, hypertensive"

class TreatmentResponse(BaseModel):
    disease_name: str
    recommended_treatment: str

# -------------------------
# Routes
# -------------------------
@router.post("/recommend", response_model=TreatmentResponse)
def recommend_treatment(request: TreatmentRequest, token: str = Depends(oauth2_scheme)):
    """
    Provide treatment recommendations for a disease.
    """
    # Verify JWT
    try:
        user_payload = verify_token(token)
        user_id = user_payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Prepare prompt for LLM
    prompt = f"Provide a detailed treatment plan for {request.disease_name}."
    if request.patient_age:
        prompt += f" The patient is {request.patient_age} years old."
    if request.patient_conditions:
        prompt += f" The patient has the following conditions: {request.patient_conditions}."

    try:
        treatment_text = llm.generate_response(prompt)
        return TreatmentResponse(
            disease_name=request.disease_name,
            recommended_treatment=treatment_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate treatment recommendation: {str(e)}")
