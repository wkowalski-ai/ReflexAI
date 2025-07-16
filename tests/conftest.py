import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

# Używamy tej samej bazy co w dewelopmencie
from src.refleks_ai.database.database import get_db
from src.refleks_ai.main import app
from src.refleks_ai.models import Base

# Użyj głównej bazy danych
DATABASE_URL = config("DATABASE_URL", default="postgresql://user:password@localhost/refleks_ai")

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Stwórz tabele RAZ na początku sesji testowej
Base.metadata.create_all(bind=engine)

def override_get_db():
    """
    Zależność, która będzie używana w testach zamiast oryginalnej get_db.
    Używa tej samej bazy danych, ale w ramach transakcji testowej.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Nadpisz zależność get_db w głównej aplikacji na czas testów
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()
def client():
    """Fixture dostarczająca klienta TestClient."""
    with TestClient(app) as c:
        yield c

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