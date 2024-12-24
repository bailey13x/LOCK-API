
from fastapi import APIRouter, HTTPException
from app.models import KeyRequest, ValidationRequest
from app.utils import generate_key, save_key_to_db, validate_key_from_db, revoke_key_in_db

router = APIRouter()

@router.post("/generate")
def generate_key_endpoint(request: KeyRequest):
    """Generate a product key."""
    product_key = generate_key(request.app_id)
    save_key_to_db(product_key, request.app_id, request.user_id, request.expiration_date)
    return {"key": product_key}

@router.post("/validate")
def validate_key_endpoint(request: ValidationRequest):
    """Validate a product key."""
    is_valid = validate_key_from_db(request.key)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or revoked key.")
    return {"valid": True}

@router.post("/revoke")
def revoke_key_endpoint(request: ValidationRequest):
    """Revoke a product key."""
    revoke_key_in_db(request.key)
    return {"status": "Key revoked successfully."}
