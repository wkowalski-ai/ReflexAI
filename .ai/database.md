Schemat Bazy Danych - Refleks.AI
Wprowadzenie
Poniższy dokument opisuje strukturę bazy danych PostgreSQL dla aplikacji Refleks.AI. Projekt zakłada na start minimalną, ale przemyślaną strukturę, która będzie fundamentem pod dalszy rozwój. Zgodnie z podjętymi decyzjami, struktura programu nauczania jest na tym etapie zaszyta w logice aplikacji, a nie w bazie danych.

Tabela 1: users
Przechowuje informacje o kontach użytkowników. Tabela zawiera kompletny zestaw pól, aby zapewnić elastyczność w przyszłości.

Nazwa Kolumny	Typ Danych	Opis
id	SERIAL PRIMARY KEY	Unikalny identyfikator użytkownika (klucz główny).
email	VARCHAR(255) UNIQUE NOT NULL	Adres e-mail, używany do logowania. Musi być unikalny.
hashed_password	VARCHAR(255) NOT NULL	Zahaszowane hasło użytkownika.
username	VARCHAR(100) UNIQUE	Opcjonalna, unikalna nazwa użytkownika.
session_id	VARCHAR(100)	Identyfikator ostatniej lekcji (może być stringiem).
created_at	TIMESTAMP WITH TIME ZONE	Data i czas utworzenia konta.
updated_at	TIMESTAMP WITH TIME ZONE	Data i czas ostatniej modyfikacji konta.

Eksportuj do Arkuszy
Tabela 2: thought_diaries
Przechowuje zapisane przez użytkowników "Dzienniki Myśli" z każdej ukończonej sesji z agentem AI.

Nazwa Kolumny	Typ Danych	Opis
id	SERIAL PRIMARY KEY	Unikalny identyfikator wpisu w dzienniku (klucz główny).
user_id	INTEGER REFERENCES users(id)	Klucz obcy łączący wpis z jego autorem w tabeli users.
session_data	JSONB NOT NULL	Kompletne podsumowanie sesji zapisane w formacie JSON.
created_at	TIMESTAMP WITH TIME ZONE	Data i czas utworzenia wpisu.

Eksportuj do Arkuszy
Przykład struktury session_data (JSONB):
JSON

{
  "session_id": "week1_day3",
  "situation": "Dostałem negatywną opinię o moim projekcie.",
  "emotions": ["smutek", "złość", "rozczarowanie"],
  "automatic_thought": "Jestem beznadziejny i nic mi nie wychodzi.",
  "cognitive_distortion": "nadmierne uogólnianie",
  "alternative_thought": "To tylko jedna opinia dotycząca jednego projektu. Inne moje prace były oceniane dobrze. Mogę się z tego czegoś nauczyć."
}
Relacje i Logika
Relacja Jeden-do-Wielu: Jeden użytkownik może mieć wiele wpisów w dzienniku. Relacja jest zdefiniowana przez klucz obcy user_id w tabeli thought_diaries.

Logika Postępów: Postęp użytkownika w programie jest śledzony w logice aplikacji. Uznajemy, że lekcja jest ukończona, gdy użytkownik pomyślnie zapisze wpis w dzienniku powiązany z daną lekcją (lesson_id wewnątrz pola session_data).