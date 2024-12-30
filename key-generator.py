from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
print(f"Encryption Key: {key.decode()}")  # Save this key securely
