# backend/routes/documents.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from models.pdf_report import PDFReport
from routes.auth import verify_token, oauth2_scheme
from typing import List, Dict

router = APIRouter(prefix="/documents", tags=["Documents"])

# -------------------------
# Pydantic Models
# -------------------------
class PatientData(BaseModel):
    name: str
    age: int
    condition: str

class ReportRequest(BaseModel):
    title: str = Field(..., example="Patient Health Report")
    description: str = Field(..., example="This report summarizes the patient's health information.")
    patients: List[PatientData]

# -------------------------
# Routes
# -------------------------
@router.post("/generate")
def generate_pdf(report_request: ReportRequest, token: str = Depends(oauth2_scheme)):
    """
    Generate a PDF health report for given patient data.
    Requires a valid JWT token.
    """
    # Verify JWT token
    try:
        user_payload = verify_token(token)
        user_id = user_payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    try:
        pdf = PDFReport(filename=f"{report_request.title.replace(' ', '_')}.pdf")
        pdf.add_title(report_request.title)
        pdf.add_paragraph(report_request.description)

        # Convert patient data to table format
        table_data = [["Name", "Age", "Condition"]]
        for patient in report_request.patients:
            table_data.append([patient.name, patient.age, patient.condition])

        pdf.add_table(table_data)
        filename = pdf.save()

        return {"message": "PDF report generated successfully", "file": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
