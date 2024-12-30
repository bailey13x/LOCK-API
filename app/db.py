import os
import psycopg2
from fastapi import HTTPException
from cryptography.fernet import Fernet

# Environment variables
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
DATABASE_URL_ENCRYPTED = os.getenv("DATABASE_URL_ENCRYPTED")

# Fetch DATABASE_URL from environment variables and decrypt it
def get_decrypted_database_url():
    try:
        cipher = Fernet(ENCRYPTION_KEY)
        decrypted_url = cipher.decrypt(DATABASE_URL_ENCRYPTED.encode()).decode()
        return decrypted_url
    except Exception as e:
        raise RuntimeError("Failed to decrypt the DATABASE_URL. Ensure the encryption key and encrypted URL are correct.") from e

# Establish database connection
def get_db_connection():
    try:
        decrypted_url = get_decrypted_database_url()
        conn = psycopg2.connect(decrypted_url, sslmode="require")
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

# Initialize the database
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ProductKeys (
                id SERIAL PRIMARY KEY,
                key TEXT UNIQUE NOT NULL,
                app_id TEXT NOT NULL,
                user_id TEXT,
                is_valid BOOLEAN DEFAULT TRUE,
                expiration_date DATE
            )
        """)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {e}")
    finally:
        # Ensure resources are properly closed
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()
