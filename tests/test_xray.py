# tests/test_xray.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from io import BytesIO

client = TestClient(app)
TEST_TOKEN = "your_test_jwt_here"

def test_upload_xray():
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    # Create a dummy image file
    img_bytes = BytesIO()
    from PIL import Image
    image = Image.new("RGB", (100, 100), color="white")
    image.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    
    files = {"file": ("test_xray.jpg", img_bytes, "image/jpeg")}
    response = client.post("/xray/upload", files=files, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "file" in data
    assert "prediction" in data
