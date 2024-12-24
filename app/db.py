
import os
import psycopg2
from fastapi import HTTPException

# Environment variables for database
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "your_db_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_db_password")
DB_NAME = os.getenv("DB_NAME", "your_db_name")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

def init_db():
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
