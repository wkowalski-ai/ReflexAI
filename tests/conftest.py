
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.refleks_ai.main import app
from src.refleks_ai.database.database import get_db
from src.refleks_ai.models import Base
from src.refleks_ai.security.hashing import get_password_hash

# Baza danych testowa w pamięci
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Create a clean database for each test."""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Create a TestClient for testing."""
    return TestClient(app)

@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "username": "testuser"
    }

@pytest.fixture
def authenticated_client(client, test_user_data, db_session):
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

@pytest.fixture
def page(browser):
    """Create a new page for each test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
