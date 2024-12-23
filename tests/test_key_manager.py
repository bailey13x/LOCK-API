import pytest
from lock.key_manager import generate_key, validate_key_local

def test_generate_key():
    key = generate_key("TEST")
    assert key.startswith("TEST-")
    assert len(key.split("-")) == 5

def test_validate_key_local():
    key = generate_key("TEST")
    assert validate_key_local(key, "TEST") is True
    assert validate_key_local("INVALID-KEY", "TEST") is False
