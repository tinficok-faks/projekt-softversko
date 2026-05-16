import pytest
from fastapi.testclient import TestClient
def test_create_ticket(client: TestClient, user_token: str):
    response = client.post(
        "/api/v1/tickets/",
        data={
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "priority": "high"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Ticket"
    assert response.json()["status"] == "new"
    assert response.json()["priority"] == "high"
    assert "id" in response.json()
def test_get_own_ticket(client: TestClient, user_token: str):
    create_response = client.post(
        "/api/v1/tickets/",
        data={
            "title": "My Ticket",
            "description": "My ticket description",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    ticket_id = create_response.json()["id"]
    response = client.get(
        f"/api/v1/tickets/{ticket_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == ticket_id
    assert response.json()["status"] in ["new", "seen", "assigned", "solved"]
def test_user_cannot_see_other_tickets(client: TestClient, session, user_token: str):
    from app.crud.user import create_user
    from app.crud.ticket import create_ticket
    from app.models import UserCreate, TicketCreate
    other_user = create_user(session, UserCreate(
        username="otheruser",
        email="other@example.com",
        password="password"
    ))
    ticket = create_ticket(
        session,
        TicketCreate(title="Other Ticket", description="Not yours"),
        other_user.id
    )
    response = client.get(
        f"/api/v1/tickets/{ticket.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
def test_list_user_tickets(client: TestClient, user_token: str):
    for i in range(3):
        client.post(
            "/api/v1/tickets/",
            data={
                "title": f"Ticket {i}",
                "description": f"Description {i}",
                "priority": "low"
            },
            headers={"Authorization": f"Bearer {user_token}"}
        )
    response = client.get(
        "/api/v1/tickets/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 3
def test_update_ticket_status(client: TestClient, user_token: str, admin_token: str):
    create_response = client.post(
        "/api/v1/tickets/",
        data={
            "title": "Status Test",
            "description": "Testing status update",
            "priority": "medium"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    ticket_id = create_response.json()["id"]
    response = client.patch(
        f"/api/v1/tickets/{ticket_id}/status",
        params={"status": "seen"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "seen"
def test_prevent_duplicate_assignment(client: TestClient, user_token: str, admin_token: str, test_support_user):
    create_response = client.post(
        "/api/v1/tickets/",
        data={
            "title": "Assignment Test",
            "description": "Testing FZ-10",
            "priority": "high"
        },
        headers={"Authorization": f"Bearer {user_token}"}
    )
    ticket_id = create_response.json()["id"]
    response1 = client.patch(
        f"/api/v1/tickets/{ticket_id}/assign",
        json={"support_user_id": test_support_user["id"]},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response1.status_code == 200
    response2 = client.patch(
        f"/api/v1/tickets/{ticket_id}/assign",
        json={"support_user_id": test_support_user["id"]},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response2.status_code == 400
    assert "already assigned" in response2.json()["detail"]