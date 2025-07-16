
import pytest
from playwright.sync_api import expect


@pytest.mark.skip(reason="Playwright needs to be installed with: playwright install")
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


@pytest.mark.skip(reason="Playwright needs to be installed with: playwright install")
def test_end_session_flow(page):
    """Test zakończenia sesji czatu."""
    # Mockuj odpowiedź dla zakończenia sesji
    def handle_end_session(route):
        route.fulfill(
            status=201,
            content_type="application/json",
            body='{"message": "Session ended successfully"}'
        )
    
    page.route("**/chat/end_session", handle_end_session)
    
    # Programowo zaloguj użytkownika
    page.goto("http://localhost:5000")
    page.evaluate("""
        localStorage.setItem('authToken', 'fake-token-for-testing');
        window.currentToken = 'fake-token-for-testing';
    """)
    page.reload()
    
    # Sprawdź czy przycisk "Zakończ i Zapisz" jest widoczny
    expect(page.locator("#end-session")).to_be_visible()
    
    # Kliknij przycisk zakończenia sesji
    page.locator("#end-session").click()
    
    # Sprawdź czy pojawił się komunikat o sukcesie
    expect(page.locator(".notification.success")).to_be_visible()
    expect(page.locator(".notification.success")).to_contain_text("Sesja została zapisana")
    
    # Sprawdź czy kontener czatu został wyczyszczony
    expect(page.locator("#chat-container")).to_be_empty()


@pytest.mark.skip(reason="Playwright needs to be installed with: playwright install")
def test_chat_unauthorized_redirect(page):
    """Test przekierowania na stronę logowania przy braku autoryzacji."""
    # Mockuj odpowiedź 401 dla endpointu czatu
    def handle_unauthorized(route):
        route.fulfill(status=401)
    
    page.route("**/chat/conversation", handle_unauthorized)
    
    # Przejdź na stronę bez logowania
    page.goto("http://localhost:5000")
    
    # Spróbuj wysłać wiadomość (jeśli interfejs jest widoczny)
    if page.locator("#chat-input").is_visible():
        page.locator("#chat-input").fill("Test message")
        page.locator(".btn-send").click()
        
        # Sprawdź czy pojawił się komunikat o błędzie i przekierowanie
        expect(page.locator(".notification.error")).to_be_visible()
        expect(page.locator("#auth-container")).to_be_visible()
