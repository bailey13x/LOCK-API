
import os
import psycopg2
from fastapi import HTTPException

# Environment variables for database
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "your_db_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_db_password")
DB_NAME = os.getenv("DB_NAME", "your_db_name")

# Fetch DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

def get_db_connection():
    try:
        # Attempt to connect using the DATABASE_URL
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}"))

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
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {e}")
    conn.commit()
    conn.close()
