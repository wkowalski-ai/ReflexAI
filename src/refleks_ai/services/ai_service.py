
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
        "model": "google/gemini-2.0-flash",
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
        "role": "system",
        "content": """Podsumuj tę sesję terapeutyczną CBT i zwróć wynik WYŁĄCZNIE w formacie JSON o następującej strukturze:
        {
            "summary_title": "Krótki tytuł sesji (max 50 znaków)",
            "session_data": {
                "situation": "Opis sytuacji, która wywołała problem",
                "automatic_thought": "Automatyczne myśli pacjenta",
                "emotion": "Emocje odczuwane przez pacjenta",
                "behavior": "Zachowania wynikające z sytuacji",
                "cognitive_distortion": "Zidentyfikowane zniekształcenia poznawcze",
                "alternative_thought": "Alternatywne, bardziej realistyczne myśli",
                "action_plan": "Plan działania na przyszłość"
            }
        }
        Odpowiedz TYLKO JSON, bez dodatkowego tekstu."""
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
        "model": "google/gemini-2.0-flash",
        "messages": extended_history
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        
        data = response.json()
        ai_response = data["choices"][0]["message"]["content"]
        
        # Parsuj odpowiedź JSON
        return json.loads(ai_response)
