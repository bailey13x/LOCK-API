# lock/key_manager.py

import random
import hashlib
from cryptography.fernet import Fernet

# Encryption key file
SECRET_FILE = "secret.key"
PRODUCT_KEY_FILE = "product.key"

def generate_key(app_id: str) -> str:
    """Generate a product key with checksum."""
    segments = ["".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4)) for _ in range(3)]
    key_body = f"{app_id}-{'-'.join(segments)}"
    checksum = hashlib.sha256(key_body.encode()).hexdigest()[:8].upper()
    return f"{key_body}-{checksum}"

def validate_key_local(key: str, app_id: str) -> bool:
    """Validate the product key locally."""
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

# Secure local storage functions
def generate_encryption_key():
    """Generate and save an encryption key."""
    key = Fernet.generate_key()
    with open(SECRET_FILE, "wb") as key_file:
        key_file.write(key)

def load_encryption_key():
    """Load the encryption key from file."""
    with open(SECRET_FILE, "rb") as key_file:
        return key_file.read()

def save_key_encrypted(product_key: str):
    """Encrypt and save the product key locally."""
    encryption_key = load_encryption_key()
    fernet = Fernet(encryption_key)
    encrypted_key = fernet.encrypt(product_key.encode())
    with open(PRODUCT_KEY_FILE, "wb") as key_file:
        key_file.write(encrypted_key)

def load_key_decrypted() -> str:
    """Decrypt and load the product key."""
    encryption_key = load_encryption_key()
    fernet = Fernet(encryption_key)
    with open(PRODUCT_KEY_FILE, "rb") as key_file:
        encrypted_key = key_file.read()
    return fernet.decrypt(encrypted_key).decode()
