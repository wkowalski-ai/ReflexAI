Plan Implementacji Projektu "Refleks.AI" w Replit
Etap 0: Przygotowanie Środowiska i Fundamentów
Celem tego etapu jest stworzenie stabilnego i zorganizowanego środowiska pracy.

Krok 0.1: Inicjalizacja Projektu w Replit

Stwórz nowy projekt w Replit, wybierając szablon Python.

W zakładce Tools > Git zainicjalizuj repozytorium Git.

Stwórz nowe, puste repozytorium na GitHubie i połącz je ze swoim projektem w Replit.

Krok 0.2: Konfiguracja Zależności

W pliku pyproject.toml (lub requirements.txt) zdefiniuj podstawowe zależności: fastapi, uvicorn[standard], sqlalchemy, psycopg2-binary, alembic, python-jose[cryptography], passlib[bcrypt], python-decouple.

Krok 0.3: Konfiguracja Sekretów

W zakładce Tools > Secrets w Replit zdefiniuj zmienne środowiskowe, których będziesz potrzebować: DATABASE_URL (pobierz z zakładki PostgreSQL), SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, OPENROUTER_API_KEY.

Krok 0.4: Ustawienie Struktury Projektu

Stwórz podstawową strukturę katalogów w projekcie, np.: /database, /routers, /models, /schemas, /static.

Etap 1: Backend - Baza Danych i CRUD
Celem jest stworzenie działającego "szkieletu" API bez logiki AI.

Krok 1.1: Zdefiniowanie Modeli Bazy Danych

W pliku w katalogu /models zdefiniuj modele SQLAlchemy:

User: z polami id, email, hashed_password, username, created_at, updated_at. Usuwamy current_lesson_id.

ThoughtDiary: z polami id, user_id (klucz obcy), summary_title (VARCHAR), session_data (JSONB), created_at.

Krok 1.2: Konfiguracja i Uruchomienie Migracji

Skonfiguruj Alembic do pracy z Twoją bazą danych w Replit.

Wygeneruj pierwszą migrację (alembic revision --autogenerate) i uruchom ją (alembic upgrade head), aby stworzyć tabele w bazie PostgreSQL.

Krok 1.3: Implementacja CRUD dla Dziennika

Stwórz router dla thought_diaries.

Zaimplementuj pełne operacje CRUD, które będą wymagały autentykacji:

GET /diaries: Pobiera listę dzienników zalogowanego użytkownika (tylko id, summary_title, created_at).

GET /diaries/{diary_id}: Pobiera szczegóły jednego wpisu.

PATCH /diaries/{diary_id}: Aktualizuje tylko pole summary_title.

DELETE /diaries/{diary_id}: Usuwa wpis.

Etap 2: Implementacja Autentykacji
Celem jest zabezpieczenie aplikacji i umożliwienie użytkownikom posiadania kont.

Krok 2.1: Rejestracja i Logowanie

Stwórz router do obsługi autentykacji.

Zaimplementuj endpoint POST /register do tworzenia nowych użytkowników.

Zaimplementuj endpoint POST /login do generowania tokenów JWT dla istniejących użytkowników.

Krok 2.2: Zabezpieczenie Endpointów

Stwórz funkcję zależności w FastAPI (get_current_user), która weryfikuje token JWT i zwraca dane zalogowanego użytkownika.

Zabezpiecz wszystkie endpointy CRUD z Etapu 1, aby wymagały poprawnego tokenu.

Krok 2.3: Testy dla Autentykacji

Napisz testy jednostkowe w pytest dla logiki rejestracji, logowania i weryfikacji tokenów.

Etap 3: Integracja z AI i Logika Sesji
Celem jest ożywienie aplikacji poprzez dodanie interakcji z modelem językowym.

Krok 3.1: Stworzenie Routera Sesji

Stwórz nowy router, np. /chat.

Zaimplementuj endpoint POST /chat/session, który rozpocznie i będzie kontynuował rozmowę.

Krok 3.2: Implementacja Logiki Konwersacji (Stateless)

Wewnątrz endpointu, zarządzaj historią rozmowy w prostej liście słowników.

Po otrzymaniu wiadomości od użytkownika, dołącz ją do historii, a następnie wyślij całą historię do API OpenRouter, aby uzyskać odpowiedź od Gemini 1.5 Flash.

Krok 3.3: Zakończenie i Zapis Sesji

Przewidź w logice, jak użytkownik kończy sesję (np. wpisując "koniec" lub klikając przycisk w UI).

Po zakończeniu sesji, sformatuj jej przebieg do ustalonej struktury JSON, wygeneruj summary_title i zapisz całość w bazie danych, tworząc nowy wpis w tabeli thought_diaries.

Etap 4: Interfejs Użytkownika (UI)
Celem jest stworzenie prostego, interaktywnego interfejsu, który komunikuje się z naszym API.

Krok 4.1: Stworzenie Podstawowych Plików

W katalogu /static stwórz index.html, style.css i script.js.

Skonfiguruj w FastAPI serwowanie plików statycznych.

Krok 4.2: Logika w JavaScript

Napisz kod JS do obsługi formularzy rejestracji i logowania (zapisywanie tokenu JWT w localStorage).

Zbuduj interfejs czatu, który dynamicznie wyświetla wiadomości i wysyła zapytania do endpointu /chat/session.

Stwórz widok "Dziennika Sesji", który pobiera dane z GET /diaries i wyświetla je jako listę.

Zaimplementuj logikę dla edycji tytułu i usuwania wpisów.

Krok 4.3: Wykorzystanie htmx/Alpine.js

Zintegruj wybraną bibliotekę, aby uprościć interakcje (np. użyj htmx do odświeżania listy dziennika bez przeładowywania całej strony).

Etap 5: Finalizacja, Testy i Wdrożenie
Celem jest zapewnienie jakości i opublikowanie działającej aplikacji.

Krok 5.1: Pełne Testowanie

Przetestuj manualnie cały przepływ użytkownika: od rejestracji, przez sesję z AI, po zarządzanie dziennikiem.

Uzupełnij testy automatyczne o najważniejsze przypadki użycia.

Krok 5.2: Konfiguracja CI/CD

Stwórz plik .github/workflows/ci.yml, który będzie uruchamiał pytest po każdym pushu na GitHubie.

Krok 5.3: Konfiguracja Uruchomienia w Replit

W pliku .replit upewnij się, że polecenie run poprawnie uruchamia serwer Uvicorn.

Sprawdź, czy aplikacja jest dostępna publicznie pod adresem URL Twojego projektu.

Krok 5.4: Zbieranie Feedbacku

Udostępnij aplikację znajomym (lub prowadzącemu kurs) i zbierz pierwsze opinie.