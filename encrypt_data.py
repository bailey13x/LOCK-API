from cryptography.fernet import Fernet

key = b"<your key>"  # Replace with the generated key
cipher = Fernet(key)
encrypted_data = cipher.encrypt(b"<your DATABASE_URL_ENCRYPTED>")
print(f"Encrypted Data: {encrypted_data.decode()}")


