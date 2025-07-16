import pytest
from fastapi.testclient import TestClient
from datetime import datetime


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


def test_get_diaries_empty(authenticated_client):
    """Test pobierania pustej listy dzienników."""
    client, token = authenticated_client

    response = client.get("/diaries")

    assert response.status_code == 200
    assert response.json() == []