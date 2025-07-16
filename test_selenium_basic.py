
#!/usr/bin/env python3

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_selenium_basic():
    """Najprostszy test sprawdzający czy Selenium działa."""
    
    # Konfiguracja Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,720")
    
    # Próba uruchomienia przeglądarki
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✓ Chrome WebDriver uruchomiony pomyślnie")
        
        # Test podstawowej funkcjonalności
        driver.get("https://www.google.com")
        print(f"✓ Załadowano stronę: {driver.title}")
        
        # Sprawdź czy możemy znaleźć element
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("test selenium")
        print("✓ Udało się wysłać tekst do pola wyszukiwania")
        
        print(f"✓ URL strony: {driver.current_url}")
        
        driver.quit()
        print("✓ Przeglądarka zamknięta pomyślnie")
        
        return True
        
    except Exception as e:
        print(f"✗ Błąd Selenium: {e}")
        return False

if __name__ == "__main__":
    test_selenium_basic()
