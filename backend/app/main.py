from fastapi import FastAPI
from app.config import settings
from app.database import create_db_and_tables

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Radi"}
