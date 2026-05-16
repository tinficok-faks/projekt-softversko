import pytest
from fastapi.testclient import TestClient
def test_register(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    assert response.json()["email"] == "new@example.com"
    assert "password" not in response.json()
def test_register_duplicate_username(client: TestClient, test_user):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "another@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
def test_login_success(client: TestClient, test_user):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert response.json()["role"] == "user"
def test_login_invalid_password(client: TestClient, test_user):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]
def test_login_nonexistent_user(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent",
            "password": "password123"
        }
    )
    assert response.status_code == 401