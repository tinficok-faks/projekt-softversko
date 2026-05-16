import pytest
from fastapi.testclient import TestClient
def test_list_all_users_admin_only(client: TestClient, user_token: str, admin_token: str):
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_change_user_role(client: TestClient, admin_token: str, session):
    from app.crud.user import create_user
    from app.models import UserCreate
    user = create_user(session, UserCreate(
        username="roletest",
        email="role@example.com",
        password="password"
    ))
    response = client.patch(
        f"/api/v1/admin/users/{user.id}/role",
        params={"role": "support"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["role"] == "support"
def test_get_statistics(client: TestClient, user_token: str, admin_token: str):
    response = client.get(
        "/api/v1/admin/statistics",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
    response = client.get(
        "/api/v1/admin/statistics",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert "total_tickets" in response.json()
def test_admin_filter_tickets_by_status(client: TestClient, user_token: str, admin_token: str):
    for i in range(3):
        client.post(
            "/api/v1/tickets/",
            json={
                "title": f"Ticket {i}",
                "description": f"Description {i}",
                "priority": "low"
            },
            headers={"Authorization": f"Bearer {user_token}"}
        )
    response = client.get(
        "/api/v1/admin/tickets?status=new",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert all(ticket["status"] == "new" for ticket in response.json())