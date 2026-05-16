from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import create_db_and_tables
from app.api.v1 import admin, auth, tickets

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Radi", "docs": "/docs", "redoc": "/redoc"}

@app.get("/health")
def health():
    return {"status": "ok"}
