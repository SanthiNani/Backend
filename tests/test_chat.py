# tests/test_chat.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
TEST_TOKEN = "your_test_jwt_here"  # Replace with valid token

def test_chat_endpoint():
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    payload = {"message": "Hello, how are you?"}
    response = client.post("/chat/", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
