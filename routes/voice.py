# backend/routes/voice.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from utils.voice_assistant import transcribe_audio_file, summarize_medical_query, audio_response
import shutil
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads/voice"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/query")
async def voice_query(file: UploadFile = File(None), text: str = Form(None)):
    """
    Handles patient queries via:
    1. Uploaded audio file
    2. Direct text input
    Returns a medical summary (and optional audio response).
    """

    # Case 1: Audio file upload
    if file:
        if not file.filename.lower().endswith((".wav", ".mp3")):
            raise HTTPException(status_code=400, detail="Invalid file type. Only WAV or MP3 allowed.")
        
        # Save uploaded audio
        file_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribe and summarize
        try:
            summary = summarize_medical_query(file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Voice processing failed: {e}")
        finally:
            os.remove(file_path)  # remove uploaded file

        return {"status": "success", "summary": summary}

    # Case 2: Text input
    elif text:
        from models.health_llm import HealthLLM
        llm = HealthLLM()
        summary = llm.generate_text(text)
        return {"status": "success", "summary": summary}

    else:
        raise HTTPException(status_code=400, detail="No audio file or text input provided.")
