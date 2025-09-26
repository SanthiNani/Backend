# tests/test_analytics.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
TEST_TOKEN = "your_test_jwt_here"

def test_generate_summary():
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    payload = {
        "patients": [
            {"name": "John", "age": 30, "symptoms": ["cough", "fever"]},
            {"name": "Jane", "age": 25, "symptoms": ["fever"]}
        ]
    }
    response = client.post("/analytics/summary", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_patients" in data
    assert "average_age" in data
    assert "symptom_summary" in data
