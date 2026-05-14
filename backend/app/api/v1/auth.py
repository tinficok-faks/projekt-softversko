from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.models import UserCreate, UserRead
from app.database import get_session
from app.security import create_access_token, hash_password
from app.crud.user import create_user, authenticate_user, get_user_by_username, get_user_by_email
from app.config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)

def register(user_create: UserCreate, session: Session = Depends(get_session)):
    return
    
@router.post("/login")

def login(username: str, password: str, session: Session = Depends(get_session)):
    ##
    return