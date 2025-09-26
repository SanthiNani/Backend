# backend/routes/xray.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from models.xray_analysis import analyze_xray
import shutil
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads/xray"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze")
async def analyze_xray_route(file: UploadFile = File(...)):
    """
    Upload an X-ray image and get predictions + dynamic summary.
    """
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PNG, JPG, JPEG allowed.")

    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Analyze X-ray
    try:
        result = analyze_xray(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"X-ray analysis failed: {e}")

    # Remove uploaded file after processing (optional)
    os.remove(file_path)

    return {
        "status": "success",
        "predictions": result["predictions"],
        "summary": result["summary"]
    }
