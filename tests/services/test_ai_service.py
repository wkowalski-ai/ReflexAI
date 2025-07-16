import pytest
from unittest.mock import AsyncMock, patch
from src.refleks_ai.services.ai_service import get_ai_response, summarize_session


@pytest.mark.asyncio
async def test_get_ai_response_success():
    """Test udanego zapytania do AI."""
    mock_history = [
        {"role": "system", "content": "Jesteś terapeutą"},
        {"role": "user", "content": "Czuję się źle"}
    ]

    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "Rozumiem, że czujesz się źle. Możesz mi powiedzieć więcej?"
                }
            }
        ]
    }

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response_obj = AsyncMock()
        mock_response_obj.json.return_value = mock_response
        mock_post.return_value = mock_response_obj

        result = await get_ai_response(mock_history)

        # Sprawdzamy, czy zwrócony tekst zgadza się z mockiem
        expected_content = "Rozumiem, że czujesz się źle. Możesz mi powiedzieć więcej?"
        assert result == expected_content

        # Sprawdź czy post został wywołany z poprawnymi argumentami
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]["json"]["model"] == "google/gemini-2.5-flash"
        assert call_args[1]["json"]["messages"] == mock_history


@pytest.mark.asyncio
async def test_summarize_session_adds_prompt():
    """Test czy summarize_session dodaje odpowiedni prompt systemowy."""
    mock_history = [
        {"role": "system", "content": "Jesteś terapeutą"},
        {"role": "user", "content": "Czuję się źle"},
        {"role": "assistant", "content": "Rozumiem"}
    ]

    mock_response = {
        "choices": [
            {
                "message": {
                    "content": '''{"summary_title": "Test", "session_data": {"situation": "Test situation"}}'''
                }
            }
        ]
    }

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response_obj = AsyncMock()
        mock_response_obj.json.return_value = mock_response
        mock_post.return_value = mock_response_obj

        result = await summarize_session(mock_history)

        # Sprawdź czy wynik został sparsowany
        assert "summary_title" in result
        assert "session_data" in result

        # Sprawdź czy post został wywołany
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        # Sprawdź czy historia została rozszerzona o prompt
        sent_messages = call_args[1]["json"]["messages"]
        assert len(sent_messages) == len(mock_history) + 1

        # Sprawdź czy ostatnia wiadomość to prompt systemowy
        last_message = sent_messages[-1]
        assert last_message["role"] == "user"
        assert "JSON" in last_message["content"]
        assert "summary_title" in last_message["content"]


@pytest.mark.asyncio
async def test_summarize_session_json_error():
    """Test obsługi błędu JSON w summarize_session."""
    mock_history = [
        {"role": "user", "content": "Test"}
    ]

    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "Invalid JSON response"
                }
            }
        ]
    }

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response_obj = AsyncMock()
        mock_response_obj.json.return_value = mock_response
        mock_post.return_value = mock_response_obj

        result = await summarize_session(mock_history)

        # Sprawdź czy zwrócono domyślną strukturę
        assert result["summary_title"] == "Sesja terapeutyczna - błąd podsumowania"
        assert "Nie udało się automatycznie" in result["session_data"]["situation"]