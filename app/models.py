
from pydantic import BaseModel

class KeyRequest(BaseModel):
    app_id: str
    user_id: str = None
    expiration_date: str = None

class ValidationRequest(BaseModel):
    key: str
