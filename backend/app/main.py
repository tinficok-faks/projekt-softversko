import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import create_db_and_tables
from app.api.v1 import auth, tickets, users

os.makedirs("uploads", exist_ok=True)
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(users.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Radi", "docs": "/docs", "redoc": "/redoc"}

@app.get("/health")
def health():
    return {"status": "ok"}
