# Projekt: Refleks.AI - Specyfikacja MVP

## 1. Główny problem

Użytkownicy często doświadczają negatywnych myśli, ale brakuje im natychmiastowego, prywatnego i ustrukturyzowanego narzędzia do ich analizy. Aplikacja Refleks.AI oferuje zawsze dostępnego asystenta AI, który prowadzi użytkownika przez kluczowe techniki terapii poznawczo-behawioralnej (CBT).

## 2. Minimalny Zestaw Funkcjonalności (MVP)

### 2.1. Autentykacja Użytkownika (Auth)
- Endpointy: `/register`, `/login` w FastAPI.
- Metoda: Autentykacja oparta na tokenach JWT.
- Zabezpieczenie: Wszystkie pozostałe endpointy wymagają ważnego tokenu.

### 2.2. Główna Logika Biznesowa (Czat z Agentem AI)
- Endpoint: `/chat`.
- Logika: Agent AI prowadzi zalogowanego użytkownika przez jeden cykl "Dziennika Myśli" CBT.
- Kontekst: Historia bieżącej rozmowy jest utrzymywana w celu zapewnienia spójności sesji.

### 2.3. Operacje CRUD na "Dziennikach Myśli"
- **CREATE**: `POST /diaries` - Zapisuje podsumowanie ukończonej sesji w bazie danych, powiązane z użytkownikiem.
- **READ**: `GET /diaries` - Zwraca listę wszystkich zapisanych dzienników dla zalogowanego użytkownika.
- **DELETE**: `DELETE /diaries` - Usuwa wpis z dziennika dla zalogowanego użytkownika.

### 2.4. Testy
- Framework: `pytest`.
- Zakres: Minimum jeden test jednostkowy (np. dla funkcji pomocniczej w autentykacji) oraz testy dla endpointów przy użyciu `TestClient`.

### 2.5. Automatyzacja CI/CD
- Narzędzie: GitHub Actions.
- Scenariusz: Automatyczne uruchamianie testów po `push` do głównej gałęzi repozytorium.

## 3. Co NIE wchodzi w zakres MVP
- Operacje **Update** i **Delete** dla dzienników.
- Zarządzanie profilem użytkownika (np. edycja, reset hasła).
- Zaawansowane role i uprawnienia.
- Rozbudowany interfejs graficzny (frontend).