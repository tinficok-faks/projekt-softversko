from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.models import User, UserRead
from app.database import get_session
from app.dependencies import get_current_admin
from app.crud.user import get_users_by_role

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/support", response_model=List[UserRead])
def get_support_users(
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    return get_users_by_role(session, "support")
