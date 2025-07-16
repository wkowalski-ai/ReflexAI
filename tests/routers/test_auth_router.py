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


def test_login_success(authenticated_client):
    """Test udanego logowania."""
    client, token = authenticated_client
    # Jeśli dotarliśmy tutaj, logowanie już się udało w fixture
    assert token is not None
    assert len(token) > 0