
import pytest
from playwright.sync_api import expect


def test_registration_flow(page):
    """Test przepływu rejestracji użytkownika."""
    # Przejdź na stronę główną
    page.goto("http://localhost:5000")
    
    # Kliknij link "Zarejestruj się"
    page.locator("#show-register").click()
    
    # Wypełnij formularz rejestracji
    page.locator("#register-form input[name='email']").fill("test@example.com")
    page.locator("#register-form input[name='username']").fill("testuser")
    page.locator("#register-form input[name='password']").fill("testpassword123")
    
    # Kliknij przycisk rejestracji
    page.locator("#register-form button[type='submit']").click()
    
    # Sprawdź czy pojawił się komunikat o sukcesie
    expect(page.locator(".notification.success")).to_be_visible()
    expect(page.locator(".notification.success")).to_contain_text("Rejestracja udana")
    
    # Sprawdź czy przełączył się na formularz logowania
    expect(page.locator("#login-section")).to_have_class("active")


def test_login_flow(page):
    """Test przepływu logowania użytkownika."""
    # Przejdź na stronę główną
    page.goto("http://localhost:5000")
    
    # Wypełnij formularz logowania (zakładając że użytkownik już istnieje)
    page.locator("#login-form input[name='email']").fill("test@example.com")
    page.locator("#login-form input[name='password']").fill("testpassword123")
    
    # Kliknij przycisk logowania
    page.locator("#login-form button[type='submit']").click()
    
    # Sprawdź czy pojawił się komunikat o sukcesie
    expect(page.locator(".notification.success")).to_be_visible()
    expect(page.locator(".notification.success")).to_contain_text("Zalogowano pomyślnie")
    
    # Sprawdź czy przełączył się na interfejs aplikacji
    expect(page.locator("#app-container")).to_be_visible()
    expect(page.locator("#auth-container")).to_have_class("hidden")
    
    # Sprawdź czy widoczny jest interfejs czatu
    expect(page.locator("#chat-container")).to_be_visible()
    expect(page.locator("#chat-input")).to_be_visible()


def test_failed_login(page):
    """Test nieudanego logowania."""
    page.goto("http://localhost:5000")
    
    # Wypełnij formularz logowania błędnymi danymi
    page.locator("#login-form input[name='email']").fill("wrong@example.com")
    page.locator("#login-form input[name='password']").fill("wrongpassword")
    
    # Kliknij przycisk logowania
    page.locator("#login-form button[type='submit']").click()
    
    # Sprawdź czy pojawił się komunikat o błędzie
    expect(page.locator(".notification.error")).to_be_visible()
    expect(page.locator(".notification.error")).to_contain_text("Błąd podczas logowania")
    
    # Sprawdź czy nadal jest widoczny formularz logowania
    expect(page.locator("#auth-container")).to_be_visible()
    expect(page.locator("#app-container")).to_have_class("hidden")
