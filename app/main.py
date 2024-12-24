from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import hashlib
import random
import os

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app with PostgreSQL!"}

# PostgreSQL Connection Setup
DB_HOST = os.getenv("DB_HOST", "dpg-ctlam61opnds73858d9g-a")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "lock_database")
DB_PASSWORD = os.getenv("DB_PASSWORD", "5jg2OaPfPdQCr06lmEpw6burFA6zEln4")
DB_NAME = os.getenv("DB_NAME", "lock_database")

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

# Initialize Database (Run Once)
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

init_db()  # Ensure table is created

# Utility Functions
def generate_key(app_id: str) -> str:
    """Generate a product key with a checksum."""
    segments = ["".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4)) for _ in range(3)]
    key_body = f"{app_id}-{'-'.join(segments)}"
    checksum = hashlib.sha256(key_body.encode()).hexdigest()[:8].upper()
    return f"{key_body}-{checksum}"

def save_key_to_db(product_key: str, app_id: str, user_id: str = None, expiration_date: str = None):
    """Save a product key to the PostgreSQL database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO ProductKeys (key, app_id, user_id, is_valid, expiration_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (product_key, app_id, user_id, True, expiration_date))
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Key already exists.")
    finally:
        conn.close()

def validate_key_from_db(product_key: str) -> bool:
    """Validate a product key from the PostgreSQL database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_valid FROM ProductKeys WHERE key = %s", (product_key,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0]

def revoke_key_in_db(product_key: str):
    """Revoke a product key in the PostgreSQL database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ProductKeys SET is_valid = FALSE WHERE key = %s", (product_key,))
    conn.commit()
    conn.close()

# API Models
class KeyRequest(BaseModel):
    app_id: str
    user_id: str = None
    expiration_date: str = None

class ValidationRequest(BaseModel):
    key: str

# API Endpoints
@app.post("/generate")
def generate_key_endpoint(request: KeyRequest):
    """Generate a product key."""
    product_key = generate_key(request.app_id)
    save_key_to_db(product_key, request.app_id, request.user_id, request.expiration_date)
    return {"key": product_key}

@app.post("/validate")
def validate_key_endpoint(request: ValidationRequest):
    """Validate a product key."""
    is_valid = validate_key_from_db(request.key)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or revoked key.")
    return {"valid": True}

@app.post("/revoke")
def revoke_key_endpoint(request: ValidationRequest):
    """Revoke a product key."""
    revoke_key_in_db(request.key)
    return {"status": "Key revoked successfully."}
