
from fastapi import FastAPI
from app.routers import keys
from app.db import init_db

# Initialize FastAPI app
app = FastAPI()

# Include routes
app.include_router(keys.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to your Lock API!"}

# Database initialization
@app.on_event("startup")
def startup_event():
    init_db()
