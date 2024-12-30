from cryptography.fernet import Fernet

key = b"NFEqx6ptrBHLwfMLGs1hOyjXpFwW9iRR8b2UvtJV5bs="  # Replace with the generated key
cipher = Fernet(key)
encrypted_data = cipher.encrypt(b"postgresql://lock_database_user:5jg2OaPfPdQCr06lmEpw6burFA6zEln4@dpg-ctlam61opnds73858d9g-a/lock_database")
print(f"Encrypted Data: {encrypted_data.decode()}")


