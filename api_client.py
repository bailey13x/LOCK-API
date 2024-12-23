# lock/api_client.py

import requests
from .config import API_URL

def verify_key_online(key: str, api_url: str = API_URL) -> bool:
    """Verify the product key with the remote API."""
    try:
        response = requests.post(f"{api_url}/validate", json={"key": key})
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json().get("valid", False)
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return False
