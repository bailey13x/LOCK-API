from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import hashlib
import random

# Initialize FastAPI app
app = FastAPI()

# Database setup
DB_FILE = "product_keys.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProductKeys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            app_id TEXT NOT NULL,
            user_id TEXT,
            is_valid BOOLEAN DEFAULT TRUE,
            expiration_date DATE
        )
    """)
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Utility functions
def generate_key(app_id: str) -> str:
    """Generate a product key with a checksum."""
    segments = ["".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4)) for _ in range(3)]
    key_body = f"{app_id}-{'-'.join(segments)}"
    checksum = hashlib.sha256(key_body.encode()).hexdigest()[:8].upper()
    return f"{key_body}-{checksum}"

def save_key_to_db(product_key: str, app_id: str, user_id: str = None, expiration_date: str = None):
    """Save a product key to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO ProductKeys (key, app_id, user_id, is_valid, expiration_date)
            VALUES (?, ?, ?, ?, ?)
        """, (product_key, app_id, user_id, True, expiration_date))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Key already exists.")
    finally:
        conn.close()

def validate_key_from_db(product_key: str) -> bool:
    """Validate a product key from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT is_valid FROM ProductKeys WHERE key = ?", (product_key,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0]

def revoke_key_in_db(product_key: str):
    """Revoke a product key in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE ProductKeys SET is_valid = FALSE WHERE key = ?", (product_key,))
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
    product_key = generate_key(request.app_id)
    save_key_to_db(product_key, request.app_id, request.user_id, request.expiration_date)
    return {"key": product_key}

@app.post("/validate")
def validate_key_endpoint(request: ValidationRequest):
    is_valid = validate_key_from_db(request.key)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or revoked key.")
    return {"valid": True}

@app.post("/revoke")
def revoke_key_endpoint(request: ValidationRequest):
    revoke_key_in_db(request.key)
    return {"status": "Key revoked successfully."}
