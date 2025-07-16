# Ostateczny Stos Technologiczny (Tech Stack) - Refleks.AI
---

Poniższy dokument opisuje kompletny i ostateczny stos technologiczny wybrany do budowy i wdrożenia aplikacji Refleks.AI.

## 1. Backend

* **Język:** Python (wersja 3.11+)
* **Framework:** FastAPI
* **Serwer ASGI:** Uvicorn
* **Opis:** Rdzeń aplikacji zostanie zbudowany przy użyciu wysokowydajnego, asynchronicznego frameworka FastAPI, co zapewni szybkość działania i łatwość budowy nowoczesnego API.

## 2. Baza Danych

* **System:** PostgreSQL
* **Integracja:** Wykorzystanie **wbudowanej w platformę Replit bazy danych PostgreSQL**.
* **Interakcja (ORM):** SQLAlchemy (w wersji 2.0+ ze wsparciem dla `asyncio`).
* **Migracje:** Alembic.
* **Opis:** Wybraliśmy PostgreSQL jako solidny, relacyjny system baz danych. Korzystanie z natywnej integracji w Replit znacząco upraszcza konfigurację i zarządzanie bazą w środowisku deweloperskim i produkcyjnym.

## 3. Model Językowy (LLM)

* **Dostawca / Model:** Google Gemini 2.5 Flash
* **Bramka API:** **OpenRouter**
* **Opis:** Sercem agenta AI będzie model Gemini 2.5 Flash, znany z szybkości i dużej wydajności. Dostęp do modelu będzie realizowany przez API OpenRouter, co daje nam elastyczność – w przyszłości możemy łatwo przełączać się na inne modele bez zmiany logiki w kodzie, korzystając z ujednoliconego interfejsu.

## 4. Frontend

* **Podejście:** Progresywne ulepszanie (Progressive Enhancement).
* **Technologie:** HTML5, CSS3, JavaScript (ES6+).
* **Biblioteki:** **htmx** i/lub **Alpine.js**.
* **Opis:** Zamiast budować skomplikowaną aplikację SPA, skupimy się na generowaniu widoków po stronie serwera (przez FastAPI). Dynamiczne i interaktywne elementy interfejsu użytkownika dodamy za pomocą lekkich bibliotek, takich jak htmx (do komunikacji z serwerem bez przeładowywania strony) i Alpine.js (do zarządzania stanem małych komponentów UI).

## 5. Pozostałe Kluczowe Narzędzia

* **Walidacja Danych:** Pydantic (natywnie zintegrowany z FastAPI).
* **Autentykacja:** Tokeny JWT, z wykorzystaniem biblioteki `python-jose`.
* **Testowanie:** `pytest` wraz z `TestClient` od FastAPI.
* **CI/CD (Automatyzacja):** GitHub Actions do automatycznego uruchamiania testów.
* **Środowisko / Platforma:** Replit (do developmentu i hostingu aplikacji).