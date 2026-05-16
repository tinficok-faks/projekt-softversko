import os
from pathlib import Path
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlmodel import Session
from app.models import User, Ticket, TicketCreate, TicketUpdate, TicketRead, TicketAssign, AttachmentRead
from app.database import get_session
from app.dependencies import get_current_user, get_current_support, get_current_admin
from app.crud.ticket import (
    create_ticket,
    get_ticket_by_id,
    get_user_tickets,
    get_assigned_tickets,
    get_all_tickets,
    update_ticket
)
from app.crud.attachment import create_attachment, get_ticket_attachments

router = APIRouter(prefix="/api/v1/tickets", tags=["tickets"])

@router.post("/", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_new_ticket(
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form("medium"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    file: Optional[UploadFile] = File(None)
):
    ticket_create = TicketCreate(title=title, description=description, priority=priority)
    ticket = create_ticket(session, ticket_create, current_user.id)
    if file:
        base_upload_dir = Path(__file__).resolve().parent.parent.parent.parent / "uploads"
        upload_dir = base_upload_dir / ticket.id
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.filename
        
        file.file.seek(0)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
            
        db_path = f"uploads/{ticket.id}/{file.filename}"
        create_attachment(session, file.filename, db_path, ticket.id)
    ticket.status = "new"
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

@router.get("/{ticket_id}", response_model=TicketRead)

def get_ticket(
    ticket_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    ticket = get_ticket_by_id(session, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    if current_user.role == "user":
        if ticket.created_by_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access other user's tickets"
            )
    elif current_user.role == "support":
        if ticket.assigned_to_id != current_user.id and ticket.created_by_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access unassigned tickets"
            )
    return ticket

@router.get("/", response_model=List[TicketRead])

def list_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role == "user":
        return get_user_tickets(session, current_user.id, skip, limit)
    elif current_user.role == "support":
        return get_assigned_tickets(session, current_user.id, skip, limit)
    else:
        return get_all_tickets(session, status, priority, skip, limit, "created_at")

@router.patch("/{ticket_id}/assign", response_model=TicketRead)
def assign_ticket(
    ticket_id: str,
    ticket_assign: TicketAssign,
    current_admin: User = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    ticket = get_ticket_by_id(session, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    ticket.assigned_to_id = ticket_assign.support_user_id
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

@router.patch("/{ticket_id}", response_model=TicketRead)
def update_existing_ticket(
    ticket_id: str,
    ticket_update: TicketUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    ticket = get_ticket_by_id(session, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
        
    if current_user.role == "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Users cannot update ticket status directly"
        )
    elif current_user.role == "support":
        if ticket.assigned_to_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot update unassigned tickets"
            )
            
    updated_ticket = update_ticket(session, ticket_id, ticket_update)
    return updated_ticket