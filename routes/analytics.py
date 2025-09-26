# backend/routes/analytics.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from models.analytics import HealthAnalytics
from routes.auth import verify_token, oauth2_scheme

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# -------------------------
# Pydantic Models
# -------------------------
class PatientInfo(BaseModel):
    name: str
    age: int
    symptoms: List[str] = []

class AnalyticsRequest(BaseModel):
    patients: List[PatientInfo]

class AnalyticsResponse(BaseModel):
    total_patients: int
    average_age: float
    symptom_summary: Dict[str, int]

# -------------------------
# Initialize Analytics
# -------------------------
analytics = HealthAnalytics()

# -------------------------
# Routes
# -------------------------
@router.post("/summary", response_model=AnalyticsResponse)
def generate_summary(request: AnalyticsRequest, token: str = Depends(oauth2_scheme)):
    """
    Generate health analytics summary for given patient data.
    Requires a valid JWT token.
    """
    # Verify JWT
    try:
        user_payload = verify_token(token)
        user_id = user_payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not request.patients:
        raise HTTPException(status_code=400, detail="No patient data provided")

    # Prepare data
    patient_data = [{"age": p.age, "symptoms": p.symptoms} for p in request.patients]

    # Generate statistics
    total_patients = len(patient_data)
    average_age = sum(p["age"] for p in patient_data) / total_patients

    # Summarize symptoms
    all_symptoms = [symptom for p in patient_data for symptom in p["symptoms"]]
    symptom_summary = analytics.summarize_symptoms(all_symptoms)

    return AnalyticsResponse(
        total_patients=total_patients,
        average_age=average_age,
        symptom_summary=symptom_summary
    )
