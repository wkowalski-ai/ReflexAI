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

@pytest.fixture
def authenticated_client(client, test_user_data):
    """Fixture tworząca klienta z zalogowanym użytkownikiem."""
    try:
        # Zarejestruj użytkownika
        register_response = client.post("/register", json=test_user_data)

        if register_response.status_code != 201:
            print(f"Registration failed: {register_response.json()}")
            raise Exception("Failed to register test user")

        # Zaloguj użytkownika
        login_data = {
            "username": test_user_data["email"],  # FastAPI OAuth2 używa 'username'
            "password": test_user_data["password"]
        }

        login_response = client.post("/token", data=login_data)

        if login_response.status_code != 200:
            print(f"Login failed: {login_response.json()}")
            raise Exception("Failed to login test user")

        token_data = login_response.json()
        token = token_data["access_token"]

        # Set Authorization header for the client
        client.headers.update({"Authorization": f"Bearer {token}"})

        return client, token

    except Exception as e:
        print(f"Error in authenticated_client fixture: {e}")
        raise

@pytest.fixture
def test_user_data():
    """Fixture z danymi testowego użytkownika."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }