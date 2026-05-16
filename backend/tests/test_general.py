import pytest
from fastapi.testclient import TestClient
def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "docs" in response.json()
def test_unauthorized_access(client: TestClient):
    response = client.get("/api/v1/tickets/")
    assert response.status_code == 401
def test_invalid_token(client: TestClient):
    response = client.get(
        "/api/v1/tickets/",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401