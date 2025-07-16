# Product Requirements Document (PRD): Refleks.AI
---

**Wersja:** 1.0
**Status:** W trakcie opracowywania
**Autor:** Witold Kowalski
**Data:** 15.07.2025

## 1. Wprowadzenie i Cel (Vision & Goal)

**Wizja produktu:** Refleks.AI to cyfrowe narzędzie wspierające psychoterapię, które pomaga pacjentom w praktykowaniu technik poznawczo-behawioralnych (CBT) pomiędzy sesjami. Aplikacja funkcjonuje jako ustrukturyzowany, interaktywny "zeszyt ćwiczeń", który ułatwia pracę domową zleconą przez terapeutę i pozwala na przygotowanie uporządkowanego materiału do omówienia na kolejnych spotkaniach.

**Cel:** Głównym celem aplikacji jest umożliwienie użytkownikowi **stworzenia uporządkowanego, cyfrowego dziennika myśli**, który może być wartościowym wsparciem w profesjonalnej terapii, ułatwiając omawianie konkretnych przykładów i śledzenie postępów.

## 2. Grupa Docelowa (Target Audience)

**Główny Użytkownik:**
Osoby **już korzystające z profesjonalnej psychoterapii** (szczególnie w nurcie CBT), które szukają skutecznego i dyskretnego narzędzia do odrabiania "prac domowych" i systematyzowania swoich przemyśleń między sesjami.

**Charakterystyka:**
* Posiadają już podstawową wiedzę o koncepcjach takich jak myśli automatyczne czy zniekształcenia poznawcze.
* Są zmotywowane do pracy nad sobą i cenią sobie ustrukturyzowane podejście.
* Potrzebują narzędzia, które pomoże im przekuć teorię z sesji w praktyczne ćwiczenia.

## 3. Główne Funkcjonalności (Features)

### 3.1. Ustrukturyzowany Program

**Opis:** Aplikacja będzie miała formę **ustrukturyzowanego, kilkutygodniowego programu**. Użytkownik będzie prowadzony krok po kroku przez kolejne moduły, które będą stopniowo odblokowywane.

* **Moduły Tygodniowe:** Każdy tydzień skupia się na innym aspekcie CBT (np. Tydzień 1: Wprowadzenie i identyfikacja myśli; Tydzień 2: Zniekształcenia poznawcze; Tydzień 3: Techniki reframingu).
* **Postęp Użytkownika:** System śledzi postępy użytkownika w programie, pokazując, które moduły zostały ukończone.
* **Codzienne Ćwiczenia:** Każdy moduł zawiera codzienne, krótkie ćwiczenia w formie sesji z agentem AI.

### 3.2. Sesja z Agentem AI (Core Interaction)

**Opis:** Centralnym elementem każdego ćwiczenia jest dialog z agentem AI. Kluczowe jest **rygorystyczne trzymanie się metodologii klinicznej CBT**.

* **Prowadzony Dialog:** Agent nie prowadzi luźnej rozmowy, lecz zadaje pytania zgodnie ze sprawdzonym schematem "Dziennika Myśli" (Sytuacja -> Emocje -> Myśli -> Dowody za/przeciw -> Myśl alternatywna).
* **Brak "Magii":** Agent jasno komunikuje, że jest narzędziem i programem komputerowym, unikając stwierdzeń, które mogłyby sugerować ludzką świadomość lub empatię. Jego celem jest struktura, a nie udawanie terapeuty.
* **Podsumowanie Sesji:** Każda sesja kończy się wygenerowaniem czystego, ustrukturyzowanego podsumowania, gotowego do zapisu.

### 3.3. Dziennik Terapeutyczny (Core Output)

**Opis:** Wszystkie ukończone ćwiczenia są zapisywane w formie "Dziennika Myśli", który jest głównym "produktem" pracy użytkownika w aplikacji.

* **Lista Wpisów:** Użytkownik ma dostęp do chronologicznej listy wszystkich swoich zapisanych dzienników.
* **Filtrowanie i Przeglądanie:** Możliwość filtrowania wpisów (np. po zidentyfikowanym zniekształceniu poznawczym lub dacie).
* **Funkcja Eksportu:** Kluczowa funkcja pozwalająca na wyeksportowanie wybranych wpisów (lub całego dziennika z danego okresu) do czytelnego formatu (np. PDF), który można łatwo wydrukować lub wysłać terapeucie.

### 3.4. System i Autentykacja
* **Rejestracja i Logowanie:** Bezpieczny system kont użytkowników (zgodny z MVP).
* **Prywatność Danych:** Wszystkie dane użytkownika są szyfrowane (zarówno w tranzycie, jak i w spoczynku). W polityce prywatności jasno określone jest, że dane nie są udostępniane ani wykorzystywane do trenowania modeli.

## 4. Zakres MVP (Pierwsza Wersja do Wdrożenia)

Pierwszym krokiem do realizacji tej wizji jest wdrożenie zdefiniowanego wcześniej MVP, które obejmuje:
* Podstawową autentykację użytkownika.
* Możliwość przeprowadzenia **jednej, pełnej sesji** z agentem AI.
* Funkcje **CREATE** **READ** **DELETE** dla Dziennika Myśli.
* Testy i CI/CD.

MVP stanowi fundament, na którym zostaną zbudowane funkcje programu, eksportu i filtrowania.

## 5. Kryteria Sukcesu

* **Wskaźnik Ukończenia Programu:** > 40% użytkowników, którzy rozpoczynają program, kończy go w całości.
* **Częstotliwość Użycia Funkcji Eksportu:** Co najmniej 25% aktywnych użytkowników korzysta z funkcji eksportu co najmniej raz w miesiącu.
* **Opinie Jakościowe:** Użytkownicy w opiniach wskazują, że aplikacja jest "pomocna", "ustrukturyzowana" i "przydatna w terapii".

## 6. Co Odkładamy na Później (Future Scope)

* Inne nurty terapeutyczne (np. Terapia Akceptacji i Zaangażowania - ACT).
* Zaawansowana analityka i wizualizacja trendów nastroju.
* Bezpośrednia integracja z platformami dla terapeutów.
* Grywalizacja i społeczność.
* Obsługa wielu języków.