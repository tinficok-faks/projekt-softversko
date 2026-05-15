from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.models import User, UserRead, Ticket, TicketRead
from app.database import get_session
from app.dependencies import get_current_admin
from app.crud.user import get_all_users, update_user_role
from app.crud.ticket import get_all_tickets, get_ticket_statistics

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

@router.get("/users", response_model=List[UserRead])

def list_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    return get_all_users(session, skip, limit)

@router.patch("/users/{user_id}/role")

def change_user_role(
    user_id: str,
    role: str,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    valid_roles = ["user", "support", "admin"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role must be one of: {', '.join(valid_roles)}"
        )
    updated_user = update_user_role(session, user_id, role)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.get("/statistics")

def get_statistics(
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    stats = get_ticket_statistics(session)
    return stats

@router.get("/tickets", response_model=List[TicketRead])

def list_all_tickets(
    status: str = None,
    priority: str = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    return get_all_tickets(session, status, priority, skip, limit, "created_at")