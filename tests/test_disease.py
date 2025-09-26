# tests/test_disease.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
TEST_TOKEN = "your_test_jwt_here"

def test_query_symptoms():
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    payload = {"symptoms": ["fever", "cough"]}
    response = client.post("/disease/query_symptoms", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "possible_diseases" in data

def test_get_disease_info():
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    payload = {"disease_name": "Influenza"}
    response = client.post("/disease/info", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["disease_name"] == "Influenza"
    assert "description" in data
