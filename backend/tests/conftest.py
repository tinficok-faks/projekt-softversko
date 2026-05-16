import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_session
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
@pytest.fixture
def test_user(session: Session, client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    return response.json()
@pytest.fixture
def test_support_user(session: Session, client: TestClient):
    from app.crud.user import create_user, update_user_role
    from app.models import UserCreate
    user_create = UserCreate(
        username="testsupport",
        email="support@example.com",
        password="testpass123"
    )
    user = create_user(session, user_create)
    update_user_role(session, user.id, "support")
    return {"id": user.id, "username": user.username, "role": user.role}
@pytest.fixture
def test_admin_user(session: Session, client: TestClient):
    from app.crud.user import create_user, update_user_role
    from app.models import UserCreate
    user_create = UserCreate(
        username="testadmin",
        email="admin@example.com",
        password="testpass123"
    )
    user = create_user(session, user_create)
    update_user_role(session, user.id, "admin")
    return {"id": user.id, "username": user.username, "role": user.role}
@pytest.fixture
def user_token(client: TestClient, test_user):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None
@pytest.fixture
def admin_token(client: TestClient, test_admin_user):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testadmin",
            "password": "testpass123"
        }
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None