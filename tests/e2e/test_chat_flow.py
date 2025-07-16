
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


def test_chat_session_flow(selenium_driver):
    """Test przepływu sesji czatu z mockowanym AI."""
    driver = selenium_driver
    wait = WebDriverWait(driver, 10)
    
    # Przejdź na stronę główną
    driver.get("http://localhost:5000")
    
    # Symuluj zalogowanie poprzez wykonanie JavaScript
    driver.execute_script("""
        localStorage.setItem('authToken', 'fake-token-for-testing');
        window.currentToken = 'fake-token-for-testing';
    """)
    
    # Odśwież stronę aby załadować interfejs aplikacji
    driver.refresh()
    
    # Sprawdź czy jest widoczny interfejs czatu
    chat_container = wait.until(EC.presence_of_element_located((By.ID, "chat-container")))
    assert chat_container.is_displayed()
    
    chat_input = wait.until(EC.presence_of_element_located((By.ID, "chat-input")))
    assert chat_input.is_displayed()
    
    # Mockuj odpowiedź API poprzez przechwycenie fetch
    driver.execute_script("""
        window.originalFetch = window.fetch;
        window.fetch = function(url, options) {
            if (url.includes('/chat/conversation')) {
                return Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({
                        message: {
                            role: 'assistant',
                            content: 'To jest mockowana odpowiedź AI. Jak się czujesz?'
                        }
                    })
                });
            }
            return window.originalFetch(url, options);
        };
    """)
    
    # Wpisz wiadomość w pole czatu
    test_message = "Czuję się dzisiaj smutno"
    chat_input.send_keys(test_message)
    
    # Kliknij przycisk "Wyślij"
    send_button = driver.find_element(By.CSS_SELECTOR, ".btn-send")
    send_button.click()
    
    # Sprawdź czy wiadomość użytkownika pojawiła się w czacie
    user_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".message.user")))
    assert user_message.is_displayed()
    
    user_message_text = driver.find_element(By.CSS_SELECTOR, ".message.user .message-text")
    assert test_message in user_message_text.text
    
    # Sprawdź czy odpowiedź AI pojawiła się w czacie
    assistant_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".message.assistant")))
    assert assistant_message.is_displayed()
    
    assistant_message_text = driver.find_element(By.CSS_SELECTOR, ".message.assistant .message-text")
    assert "To jest mockowana odpowiedź AI" in assistant_message_text.text
    
    # Sprawdź czy pole input zostało wyczyszczone
    assert chat_input.get_attribute("value") == ""
