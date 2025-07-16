
import pytest
from src.refleks_ai.security.hashing import hash_password, verify_password


def test_hash_password():
    """Test czy hasło jest poprawnie haszowane."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 0
    assert hashed.startswith("$2b$")


def test_verify_password_correct():
    """Test czy verify_password zwraca True dla poprawnego hasła."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test czy verify_password zwraca False dla błędnego hasła."""
    password = "testpassword123"
    wrong_password = "wrongpassword"
    hashed = hash_password(password)
    
    assert verify_password(wrong_password, hashed) is False


def test_verify_password_empty():
    """Test czy verify_password zwraca False dla pustego hasła."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    assert verify_password("", hashed) is False
