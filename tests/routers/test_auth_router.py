
import pytest
from fastapi.testclient import TestClient


def test_register_success(client, test_user_data):
    """Test udanej rejestracji użytkownika."""
    response = client.post("/register", json=test_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user_data):
    """Test rejestracji z już istniejącym emailem."""
    # Pierwsza rejestracja
    client.post("/register", json=test_user_data)
    
    # Próba ponownej rejestracji z tym samym emailem
    response = client.post("/register", json=test_user_data)
    
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"]


def test_register_invalid_email(client):
    """Test rejestracji z niepoprawnym emailem."""
    invalid_data = {
        "email": "invalid-email",
        "password": "testpassword123",
        "username": "testuser"
    }
    
    response = client.post("/register", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_login_success(authenticated_client):
    """Test udanego logowania."""
    client, token = authenticated_client
    # Jeśli dotarliśmy tutaj, logowanie już się udało w fixture
    assert token is not None
    assert len(token) > 0


def test_login_invalid_credentials(client):
    """Test logowania z błędnymi danymi."""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = client.post("/token", data=login_data)
    assert response.status_code == 401


def test_login_success_manual(client, test_user_data):
    """Test udanego logowania."""
    # Najpierw zarejestruj użytkownika
    client.post("/register", json=test_user_data)
    
    # Zaloguj się
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/token", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user_data):
    """Test logowania z błędnym hasłem."""
    # Najpierw zarejestruj użytkownika
    client.post("/register", json=test_user_data)
    
    # Próba logowania z błędnym hasłem
    login_data = {
        "username": test_user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/token", data=login_data)
    
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test logowania nieistniejącego użytkownika."""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "somepassword"
    }
    response = client.post("/token", data=login_data)
    
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]
