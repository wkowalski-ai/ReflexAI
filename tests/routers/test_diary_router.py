
import pytest
from fastapi.testclient import TestClient
from datetime import datetime


def test_get_diaries_empty(authenticated_client):
    """Test pobierania pustej listy dzienników."""
    client, token = authenticated_client
    
    response = client.get("/diaries")
    
    assert response.status_code == 200
    assert response.json() == []


def test_create_diary_success(authenticated_client):
    """Test tworzenia nowego wpisu dziennika."""
    client, token = authenticated_client
    
    diary_data = {
        "summary_title": "Test Session",
        "session_data": {
            "situation": "Test situation",
            "automatic_thought": "Test thought",
            "emotion": "Test emotion"
        }
    }
    
    response = client.post("/diaries", json=diary_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["summary_title"] == diary_data["summary_title"]
    assert data["session_data"] == diary_data["session_data"]
    assert "id" in data
    assert "created_at" in data


def test_get_diary_by_id(authenticated_client):
    """Test pobierania konkretnego wpisu dziennika."""
    client, token = authenticated_client
    
    # Najpierw utwórz wpis
    diary_data = {
        "summary_title": "Test Session",
        "session_data": {"situation": "Test situation"}
    }
    create_response = client.post("/diaries", json=diary_data)
    diary_id = create_response.json()["id"]
    
    # Pobierz wpis
    response = client.get(f"/diaries/{diary_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == diary_id
    assert data["summary_title"] == diary_data["summary_title"]


def test_get_diary_not_found(authenticated_client):
    """Test pobierania nieistniejącego wpisu."""
    client, token = authenticated_client
    
    response = client.get("/diaries/999")
    
    assert response.status_code == 404
    assert "Diary not found" in response.json()["detail"]


def test_delete_diary_success(authenticated_client):
    """Test usuwania wpisu dziennika."""
    client, token = authenticated_client
    
    # Najpierw utwórz wpis
    diary_data = {
        "summary_title": "Test Session",
        "session_data": {"situation": "Test situation"}
    }
    create_response = client.post("/diaries", json=diary_data)
    diary_id = create_response.json()["id"]
    
    # Usuń wpis
    response = client.delete(f"/diaries/{diary_id}")
    
    assert response.status_code == 204
    
    # Sprawdź czy wpis został usunięty
    get_response = client.get(f"/diaries/{diary_id}")
    assert get_response.status_code == 404


def test_delete_diary_not_found(authenticated_client):
    """Test usuwania nieistniejącego wpisu."""
    client, token = authenticated_client
    
    response = client.delete("/diaries/999")
    
    assert response.status_code == 404


def test_unauthorized_access(client):
    """Test dostępu do endpointów bez autoryzacji."""
    response = client.get("/diaries")
    assert response.status_code == 401
    
    response = client.post("/diaries", json={"summary_title": "Test"})
    assert response.status_code == 401
    
    response = client.get("/diaries/1")
    assert response.status_code == 401
    
    response = client.delete("/diaries/1")
    assert response.status_code == 401
