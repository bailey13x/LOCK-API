import pytest
from lock.api_client import verify_key_online

def test_verify_key_online(mocker):
    mocker.patch("requests.post", return_value=mocker.Mock(status_code=200, json=lambda: {"valid": True}))
    assert verify_key_online("VALID-KEY", "https://example.com/api") is True

    mocker.patch("requests.post", return_value=mocker.Mock(status_code=400, json=lambda: {"valid": False}))
    assert verify_key_online("INVALID-KEY", "https://example.com/api") is False
