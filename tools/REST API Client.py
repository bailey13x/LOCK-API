import requests

def verify_key_online(key: str, api_url: str) -> bool:
    """
    Verify the product key with a remote server.
    """
    try:
        response = requests.post(f"{api_url}/validate", json={"key": key})
        return response.status_code == 200 and response.json().get("valid", False)
    except Exception as e:
        print(f"API Error: {e}")
        return False

# Example usage (requires server setup)
if __name__ == "__main__":
    api_url = "https://example.com/api"
    test_key = generate_key("LOCK")
    print("Online Validation:", verify_key_online(test_key, api_url))
