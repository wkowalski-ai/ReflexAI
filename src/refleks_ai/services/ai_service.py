import httpx
import json
from typing import List, Dict
from decouple import config


async def get_ai_response(history: List[dict]) -> str:
    """
    Komunikuje się z OpenRouter API, aby uzyskać odpowiedź AI
    """
    api_key = config("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemini-2.5-flash",
        "messages": history
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]


async def summarize_session(history: List[dict]) -> dict:
    """
    Podsumowuje sesję czatu i zwraca strukturyzowane dane w formacie JSON
    """
    # Dodaj prompt systemowy na końcu historii
    summary_prompt = {
        "role": "user",
        "content": """WAŻNE: Musisz odpowiedzieć WYŁĄCZNIE w formacie JSON, bez żadnego dodatkowego tekstu przed ani po JSON-ie.

Przeanalizuj powyższą sesję terapeutyczną CBT i zwróć podsumowanie w DOKŁADNIE takim formacie JSON:

{
    "summary_title": "Krótki tytuł opisujący główny temat sesji (max 50 znaków)",
    "session_data": {
        "situation": "Konkretna sytuacja lub wydarzenie, które zostało omówione",
        "automatic_thought": "Główne automatyczne myśli pacjenta zidentyfikowane w sesji",
        "emotion": "Emocje odczuwane przez pacjenta w opisanej sytuacji",
        "behavior": "Zachowania pacjenta w odpowiedzi na sytuację",
        "cognitive_distortion": "Zniekształcenia poznawcze zidentyfikowane w myślach pacjenta",
        "alternative_thought": "Bardziej realistyczne i zbalansowane myśli wypracowane w sesji",
        "action_plan": "Konkretne kroki lub strategie na przyszłość"
    }
}

Jeśli któryś element nie został omówiony w sesji, wpisz "Nie omówiono w tej sesji" zamiast "Brak danych".

ODPOWIEDZ TYLKO JSON - żadnego innego tekstu!"""
    }

    # Skopiuj historię i dodaj prompt
    extended_history = history.copy()
    extended_history.append(summary_prompt)

    api_key = config("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemini-2.5-flash",
        "messages": extended_history
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        response_data = response.json()

        # Otrzymujemy odpowiedź od AI
        ai_response = response_data["choices"][0]["message"]["content"]

        # Szczegółowe logowanie dla debugowania
        print(f"=== DEBUGGING AI SUMMARY RESPONSE ===")
        print(f"Raw AI response: '{ai_response}'")
        print(f"Response length: {len(ai_response) if ai_response else 0}")
        print(f"Response type: {type(ai_response)}")

        # Sprawdź czy odpowiedź nie jest pusta
        if not ai_response or not ai_response.strip():
            print("ERROR: AI response is empty or only whitespace")
            raise ValueError("AI response is empty. Cannot decode JSON.")

        # Oczyść odpowiedź z ewentualnych białych znaków i formatowania Markdown
        cleaned_response = ai_response.strip()

        # Usuń bloki kodu Markdown jeśli istnieją
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]  # Usuń '```json'
        if cleaned_response.startswith('```'):
            cleaned_response = cleaned_response[3:]   # Usuń '```'
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]  # Usuń '```' na końcu

        cleaned_response = cleaned_response.strip()
        print(f"Cleaned response after markdown removal: '{cleaned_response}'")

        try:
            # Parsuj odpowiedź JSON
            parsed_json = json.loads(cleaned_response)
            print(f"SUCCESS: JSON parsed successfully")
            print(f"Parsed JSON: {parsed_json}")
            return parsed_json
        except json.JSONDecodeError as e:
            # Szczegółowe logowanie błędu JSON
            print(f"JSON DECODE ERROR: {str(e)}")
            print(f"Error position: line {e.lineno}, column {e.colno}")
            print(f"Failed to parse: '{cleaned_response}'")
            print(f"First 200 chars: '{cleaned_response[:200]}'")

            # Zwróć domyślną strukturę w przypadku błędu
            return {
                "summary_title": "Sesja terapeutyczna - błąd podsumowania",
                "session_data": {
                    "situation": "Nie udało się automatycznie podsumować sytuacji",
                    "automatic_thought": "Nie udało się automatycznie podsumować myśli",
                    "emotion": "Nie udało się automatycznie podsumować emocji", 
                    "behavior": "Nie udało się automatycznie podsumować zachowań",
                    "cognitive_distortion": "Nie udało się automatycznie zidentyfikować zniekształceń",
                    "alternative_thought": "Nie udało się automatycznie wygenerować alternatywnych myśli",
                    "action_plan": "Nie udało się automatycznie wygenerować planu działania"
                }
            }