from fastapi import FastAPI
from app.config import settings
from app.database import create_db_and_tables
from app.api.v1 import auth, tickets

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
)


app.include_router(auth.router)
app.include_router(tickets.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Radi"}
