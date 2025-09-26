# tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "password123"

def test_signup():
    response = client.post("/auth/signup", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data and "email" in data
    assert data["email"] == TEST_EMAIL

def test_login():
    response = client.post(
        "/auth/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_me():
    # First, login to get token
    login_resp = client.post(
        "/auth/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == TEST_EMAIL
