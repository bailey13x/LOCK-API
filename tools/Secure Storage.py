from cryptography.fernet import Fernet

# Generate a key and save it (only run once for production)
def generate_encryption_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_encryption_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

def save_key_encrypted(product_key: str):
    encryption_key = load_encryption_key()
    fernet = Fernet(encryption_key)
    encrypted_key = fernet.encrypt(product_key.encode())
    with open("product.key", "wb") as key_file:
        key_file.write(encrypted_key)

def load_key_decrypted():
    encryption_key = load_encryption_key()
    fernet = Fernet(encryption_key)
    with open("product.key", "rb") as key_file:
        encrypted_key = key_file.read()
    return fernet.decrypt(encrypted_key).decode()

# Example usage
if __name__ == "__main__":
    generate_encryption_key()  # Run only once
    test_key = generate_key("LOCK")
    save_key_encrypted(test_key)
    print("Stored Key:", load_key_decrypted())
