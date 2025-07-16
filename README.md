
# Refleks.AI 🧠

**Cyfrowe narzędzie wspierające terapię poznawczo-behawioralną (CBT)**

Refleks.AI to aplikacja webowa, która pomaga pacjentom w praktykowaniu technik CBT pomiędzy sesjami terapeutycznymi. Funkcjonuje jako ustrukturyzowany, interaktywny "zeszyt ćwiczeń", który ułatwia pracę domową zleconą przez terapeutę i pozwala na przygotowanie uporządkowanego materiału do omówienia na kolejnych spotkaniach.

## 🎯 Cel aplikacji

Głównym celem jest umożliwienie użytkownikowi **stworzenia uporządkowanego, cyfrowego dziennika myśli**, który może być wartościowym wsparciem w profesjonalnej terapii, ułatwiając omawianie konkretnych przykładów i śledzenie postępów.

## 🚀 Funkcjonalności

### Obecne (MVP)
- ✅ **Autentykacja użytkowników** - bezpieczne logowanie i rejestracja
- ✅ **Sesje z AI** - prowadzony dialog zgodny z metodologią CBT
- ✅ **Dziennik myśli** - zapis, przeglądanie i usuwanie wpisów
- ✅ **Strukturalne podejście** - każda sesja prowadzi przez schemat: Sytuacja → Emocje → Myśli → Dowody → Alternatywne myśli

### Planowane
- 📋 Ustrukturyzowany program wielotygodniowy
- 📊 Eksport dziennika do PDF
- 🔍 Filtrowanie wpisów po kategoriach
- 📈 Śledzenie postępów

## 🛠️ Technologie

### Backend
- **Python 3.11+** z frameworkiem **FastAPI**
- **PostgreSQL** jako baza danych (natywna integracja Replit)
- **SQLAlchemy 2.0** (ORM) + **Alembic** (migracje)
- **JWT** do autentykacji użytkowników

### Frontend
- **Progressive Enhancement** - HTML5, CSS3, JavaScript ES6+
- **htmx** do dynamicznych interakcji
- Responsive design

### AI
- **Google Gemini 2.5 Flash** przez **OpenRouter API**
- Specjalizacja w prowadzeniu sesji CBT

### Deployment
- **Replit** (development i hosting)
- **GitHub Actions** (CI/CD)

## 📦 Instalacja i uruchomienie

### 1. Klonowanie repozytorium
```bash
git clone <repository-url>
cd refleks-ai
```

### 2. Konfiguracja zmiennych środowiskowych
W Replit, w zakładce **Tools > Secrets**, dodaj:
```
DATABASE_URL=<twoja-postgresql-url>
SECRET_KEY=<losowy-klucz-32-znaki>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENROUTER_API_KEY=<twoj-klucz-openrouter>
```

### 3. Migracje bazy danych
```bash
alembic upgrade head
```

### 4. Uruchomienie aplikacji
Kliknij przycisk **Run** w Replit lub użyj:
```bash
uvicorn src.refleks_ai.main:app --host 0.0.0.0 --port 5000
```

Aplikacja będzie dostępna pod adresem URL twojego Replit.

## 🧪 Testy

Uruchomienie testów jednostkowych:
```bash
pytest tests/ -v
```

Testy obejmują:
- Autentykację użytkowników
- Operacje CRUD na dzienniku
- Integrację z AI
- Endpointy API

## 📁 Struktura projektu

```
src/refleks_ai/
├── database/          # Konfiguracja bazy danych
├── models/           # Modele SQLAlchemy
├── routers/          # Endpointy API (auth, chat, diary, ui)
├── schemas/          # Schematy Pydantic
├── security/         # JWT i hashing
├── services/         # Logika biznesowa (AI service)
└── main.py          # Aplikacja FastAPI

static/              # Pliki frontend (HTML, CSS, JS)
templates/           # Szablony Jinja2
tests/              # Testy jednostkowe
```

## 🎭 Jak używać aplikacji

1. **Rejestracja/Logowanie** - Utwórz konto lub zaloguj się
2. **Rozpocznij sesję** - Kliknij "Nowa rozmowa"
3. **Dialog z AI** - Opisz sytuację, która Cię niepokoi
4. **Analiza CBT** - AI poprowadzi Cię przez:
   - Identyfikację emocji
   - Rozpoznanie myśli automatycznych
   - Znalezienie zniekształceń poznawczych
   - Wypracowanie alternatywnych myśli
5. **Zapis w dzienniku** - Zakończ sesję i zapisz podsumowanie
6. **Przeglądanie** - Dostęp do wszystkich zapisanych sesji

## 🔒 Bezpieczeństwo i prywatność

- Wszystkie dane są szyfrowane (w tranzycie i spoczynku)
- Tokeny JWT z ograniczonym czasem życia
- Dane nie są udostępniane ani wykorzystywane do trenowania modeli
- Zgodność z najlepszymi praktykami bezpieczeństwa

## 🤝 Dla kogo?

Aplikacja jest przeznaczona dla osób **już korzystających z profesjonalnej psychoterapii** (szczególnie CBT), które:
- Posiadają podstawową wiedzę o myślach automatycznych i zniekształceniach poznawczych
- Są zmotywowane do pracy nad sobą
- Potrzebują narzędzia do systematyzowania przemyśleń między sesjami

## ⚠️ Ważne zastrzeżenia

- **To nie jest zastępstwo dla profesjonalnej terapii**
- Aplikacja służy jako narzędzie wspierające, nie terapeutyczne
- W przypadku kryzysu psychicznego skontaktuj się z profesjonalistą
- AI jasno komunikuje, że jest programem komputerowym, nie terapeutą

## 📄 Licencja

[Określ licencję projektu]

## 🤖 Rozwój

Projekt jest aktywnie rozwijany. Aktualne postępy i planowane funkcjonalności można śledzić w [Issues](link-do-issues).

---

**Refleks.AI** - Twój cyfrowy towarzysz w podróży ku lepszemu zdrowiu psychicznemu 🌱
