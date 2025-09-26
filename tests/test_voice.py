# tests/test_voice.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from io import BytesIO
import wave

client = TestClient(app)
TEST_TOKEN = "your_test_jwt_here"

def test_upload_voice():
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}

    # Create a dummy WAV file
    audio_bytes = BytesIO()
    with wave.open(audio_bytes, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b'\x00\x00'*1000)
    audio_bytes.seek(0)

    files = {"file": ("test_audio.wav", audio_bytes, "audio/wav")}
    response = client.post("/voice/upload", files=files, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "file" in data
    assert "transcription" in data
