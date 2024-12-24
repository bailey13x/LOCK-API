
import random
import hashlib
from app.db import get_db_connection

def generate_key(app_id: str) -> str:
    """Generate a product key with a checksum."""
    segments = ["".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4)) for _ in range(3)]
    key_body = f"{app_id}-{'-'.join(segments)}"
    checksum = hashlib.sha256(key_body.encode()).hexdigest()[:8].upper()
    return f"{key_body}-{checksum}"

def save_key_to_db(product_key: str, app_id: str, user_id: str = None, expiration_date: str = None):
    """Save a product key to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO ProductKeys (key, app_id, user_id, is_valid, expiration_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (product_key, app_id, user_id, True, expiration_date))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

def validate_key_from_db(product_key: str) -> bool:
    """Validate a product key from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_valid FROM ProductKeys WHERE key = %s", (product_key,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0]

def revoke_key_in_db(product_key: str):
    """Revoke a product key in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ProductKeys SET is_valid = FALSE WHERE key = %s", (product_key,))
    conn.commit()
    conn.close()
