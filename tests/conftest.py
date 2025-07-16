
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.refleks_ai.models import Base
from src.refleks_ai.database.database import get_db
from src.refleks_ai.main import app
from decouple import config

TEST_DATABASE_URL = config("TEST_DATABASE_URL", default="sqlite:///./test.db")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Fixture tworząca czystą bazę i sesję w transakcji dla każdego testu."""
    Base.metadata.drop_all(bind=engine) # Usuń wszystko
    Base.metadata.create_all(bind=engine) # Stwórz od nowa

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Fixture tworząca klienta API z nadpisaną zależnością bazy danych."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

# Playwright fixtures for E2E tests
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for E2E tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }

@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "username": "testuser"
    }

@pytest.fixture
def authenticated_client(client, test_user_data):
    """Create an authenticated client with a test user."""
    # Najpierw zarejestruj użytkownika
    register_response = client.post("/register", json=test_user_data)
    assert register_response.status_code == 201

    # Zaloguj się i pobierz token
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    login_response = client.post("/token", data=login_data)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Ustaw nagłówek autoryzacji
    client.headers.update({"Authorization": f"Bearer {token}"})

    return client, token
