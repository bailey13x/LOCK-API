def validate_key_local(key: str, app_id: str) -> bool:
    """
    Validate the product key locally.
    - Check format.
    - Validate checksum.
    """
    try:
        parts = key.split("-")
        if len(parts) != 5 or parts[0] != app_id:
            return False

        key_body = "-".join(parts[:-1])
        expected_checksum = parts[-1]
        calculated_checksum = hashlib.sha256(key_body.encode()).hexdigest()[:8].upper()
        return calculated_checksum == expected_checksum
    except Exception as e:
        print(f"Validation Error: {e}")
        return False


# Example usage
if __name__ == "__main__":
    test_key = generate_key("LOCK")
    print("Valid Key:", validate_key_local(test_key, "LOCK"))
