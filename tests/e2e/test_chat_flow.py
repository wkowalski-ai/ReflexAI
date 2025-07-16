import pytest
from playwright.sync_api import expect


def test_chat_session_flow(page):
    """Test przepływu sesji czatu z mockowanym AI."""
    # Mockuj odpowiedź AI
    def handle_chat_request(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"message": {"role": "assistant", "content": "To jest mockowana odpowiedź AI. Jak się czujesz?"}}'
        )

    # Przechwytuj zapytania do endpointu czatu
    page.route("**/chat/conversation", handle_chat_request)

    # Programowo zaloguj użytkownika (szybsze niż przez UI)
    page.goto("http://localhost:5000")

    # Wstrzyknij token do localStorage (symulacja logowania)
    page.evaluate("""
        localStorage.setItem('authToken', 'fake-token-for-testing');
        window.currentToken = 'fake-token-for-testing';
    """)

    # Odśwież stronę aby załadować interfejs aplikacji
    page.reload()

    # Sprawdź czy jest widoczny interfejs czatu
    expect(page.locator("#chat-container")).to_be_visible()
    expect(page.locator("#chat-input")).to_be_visible()

    # Wpisz wiadomość w pole czatu
    test_message = "Czuję się dzisiaj smutno"
    page.locator("#chat-input").fill(test_message)

    # Kliknij przycisk "Wyślij"
    page.locator(".btn-send").click()

    # Sprawdź czy wiadomość użytkownika pojawiła się w czacie
    expect(page.locator(".message.user")).to_be_visible()
    expect(page.locator(".message.user .message-text")).to_contain_text(test_message)

    # Sprawdź czy odpowiedź AI pojawiła się w czacie
    expect(page.locator(".message.assistant")).to_be_visible()
    expect(page.locator(".message.assistant .message-text")).to_contain_text("To jest mockowana odpowiedź AI")

    # Sprawdź czy pole input zostało wyczyszczone
    expect(page.locator("#chat-input")).to_have_value("")
```

```
import pytest
from playwright.sync_api import expect


def test_chat_session_flow(page):
    """Test przepływu sesji czatu z mockowanym AI."""
    # Mockuj odpowiedź AI
    def handle_chat_request(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"message": {"role": "assistant", "content": "To jest mockowana odpowiedź AI. Jak się czujesz?"}}'
        )

    # Przechwytuj zapytania do endpointu czatu
    page.route("**/chat/conversation", handle_chat_request)

    # Programowo zaloguj użytkownika (szybsze niż przez UI)
    page.goto("http://localhost:5000")

    # Wstrzyknij token do localStorage (symulacja logowania)
    page.evaluate("""
        localStorage.setItem('authToken', 'fake-token-for-testing');
        window.currentToken = 'fake-token-for-testing';
    """)

    # Odśwież stronę aby załadować interfejs aplikacji
    page.reload()

    # Sprawdź czy jest widoczny interfejs czatu
    expect(page.locator("#chat-container")).to_be_visible()
    expect(page.locator("#chat-input")).to_be_visible()

    # Wpisz wiadomość w pole czatu
    test_message = "Czuję się dzisiaj smutno"
    page.locator("#chat-input").fill(test_message)

    # Kliknij przycisk "Wyślij"
    page.locator(".btn-send").click()

    # Sprawdź czy wiadomość użytkownika pojawiła się w czacie
    expect(page.locator(".message.user")).to_be_visible()
    expect(page.locator(".message.user .message-text")).to_contain_text(test_message)

    # Sprawdź czy odpowiedź AI pojawiła się w czacie
    expect(page.locator(".message.assistant")).to_be_visible()
    expect(page.locator(".message.assistant .message-text")).to_contain_text("To jest mockowana odpowiedź AI")

    # Sprawdź czy pole input zostało wyczyszczone
    expect(page.locator("#chat-input")).to_have_value("")