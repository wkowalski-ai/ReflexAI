
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_registration_flow(selenium_driver):
    """Test przepływu rejestracji użytkownika."""
    driver = selenium_driver
    
    # Przejdź na stronę główną
    driver.get("http://localhost:5000")
    
    # Poczekaj aż strona się załaduje
    wait = WebDriverWait(driver, 10)
    
    # Kliknij link "Zarejestruj się"
    show_register = wait.until(EC.element_to_be_clickable((By.ID, "show-register")))
    show_register.click()
    
    # Wypełnij formularz rejestracji
    email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#register-form input[name='email']")))
    email_input.send_keys("test@example.com")
    
    username_input = driver.find_element(By.CSS_SELECTOR, "#register-form input[name='username']")
    username_input.send_keys("testuser")
    
    password_input = driver.find_element(By.CSS_SELECTOR, "#register-form input[name='password']")
    password_input.send_keys("testpassword123")
    
    # Kliknij przycisk rejestracji
    submit_button = driver.find_element(By.CSS_SELECTOR, "#register-form button[type='submit']")
    submit_button.click()
    
    # Sprawdź czy pojawił się komunikat o sukcesie
    success_notification = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".notification.success")))
    assert "Rejestracja udana" in success_notification.text
    
    # Sprawdź czy przełączył się na formularz logowania
    login_section = wait.until(EC.presence_of_element_located((By.ID, "login-section")))
    assert "active" in login_section.get_attribute("class")


def test_login_flow(selenium_driver):
    """Test przepływu logowania użytkownika."""
    driver = selenium_driver
    wait = WebDriverWait(driver, 10)
    
    # Przejdź na stronę główną
    driver.get("http://localhost:5000")
    
    # Wypełnij formularz logowania (zakładając że użytkownik już istnieje)
    email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#login-form input[name='email']")))
    email_input.send_keys("test@example.com")
    
    password_input = driver.find_element(By.CSS_SELECTOR, "#login-form input[name='password']")
    password_input.send_keys("testpassword123")
    
    # Kliknij przycisk logowania
    submit_button = driver.find_element(By.CSS_SELECTOR, "#login-form button[type='submit']")
    submit_button.click()
    
    # Sprawdź czy pojawił się komunikat o sukcesie
    success_notification = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".notification.success")))
    assert "Zalogowano pomyślnie" in success_notification.text
    
    # Sprawdź czy przełączył się na interfejs aplikacji
    app_container = wait.until(EC.presence_of_element_located((By.ID, "app-container")))
    assert app_container.is_displayed()
    
    auth_container = driver.find_element(By.ID, "auth-container")
    assert "hidden" in auth_container.get_attribute("class")
    
    # Sprawdź czy widoczny jest interfejs czatu
    chat_container = wait.until(EC.presence_of_element_located((By.ID, "chat-container")))
    assert chat_container.is_displayed()
    
    chat_input = driver.find_element(By.ID, "chat-input")
    assert chat_input.is_displayed()
