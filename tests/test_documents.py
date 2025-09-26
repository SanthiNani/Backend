# tests/test_documents.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
TEST_TOKEN = "your_test_jwt_here"

def test_generate_pdf():
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    payload = {
        "title": "Test Report",
        "description": "Sample report for testing",
        "patients": [{"name": "John", "age": 30, "condition": "Healthy"}]
    }
    response = client.post("/documents/generate", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "file" in data
