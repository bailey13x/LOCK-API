import random
import hashlib

def generate_key(app_id: str) -> str:
    """
    Generate a random product key with checksum.
    Format: APPID-XXXX-XXXX-XXXX-CHECKSUM
    """
    segments = ["".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4)) for _ in range(3)]
    key_body = f"{app_id}-{'-'.join(segments)}"
    checksum = hashlib.sha256(key_body.encode()).hexdigest()[:8].upper()
    return f"{key_body}-{checksum}"

# Example usage
if __name__ == "__main__":
    app_id = "LOCK"
    print("Generated Key:", generate_key(app_id))
