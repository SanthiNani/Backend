from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from routes.auth import verify_token, oauth2_scheme
from models.health_llm import HealthLLM

router = APIRouter(prefix="/disease", tags=["Disease"])

llm = HealthLLM()

class SymptomQuery(BaseModel):
    symptoms: List[str]

class DiseaseInfoRequest(BaseModel):
    disease_name: str

class DiseaseInfoResponse(BaseModel):
    disease_name: str
    description: str
    symptoms: List[str]
    treatment: str

@router.post("/query_symptoms")
def query_disease_by_symptoms(request: SymptomQuery, token: str = Depends(oauth2_scheme)):
    try:
        user_payload = verify_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if not request.symptoms:
        raise HTTPException(status_code=400, detail="No symptoms provided")
    prompt = f"List possible diseases for these symptoms: {', '.join(request.symptoms)}"
    response = llm.generate_response(prompt)
    return {"possible_diseases": response}

@router.post("/info", response_model=DiseaseInfoResponse)
def get_disease_info(request: DiseaseInfoRequest, token: str = Depends(oauth2_scheme)):
    try:
        user_payload = verify_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    prompt = f"Provide description, symptoms, treatment for {request.disease_name}"
    response_text = llm.generate_response(prompt)
    return DiseaseInfoResponse(
        disease_name=request.disease_name,
        description=response_text,
        symptoms=[],
        treatment=""
    )
