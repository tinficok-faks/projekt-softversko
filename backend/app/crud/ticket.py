from typing import Optional, List
from sqlmodel import Session, select
from app.models import Ticket, TicketCreate, TicketUpdate, TicketRead

def create_ticket(session: Session, ticket_create: TicketCreate, user_id: str) -> Ticket:
    ticket = Ticket(
        title=ticket_create.title,
        description=ticket_create.description,
        priority=ticket_create.priority,
        status="new",
        created_by_id=user_id
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

def get_ticket_by_id(session: Session, ticket_id: str) -> Optional[Ticket]:
    return session.exec(select(Ticket).where(Ticket.id == ticket_id)).first()

def get_user_tickets(session: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Ticket]:
    return session.exec(
        select(Ticket)
        .where(Ticket.created_by_id == user_id)
        .offset(skip)
        .limit(limit)
    ).all()

def get_assigned_tickets(session: Session, support_id: str, skip: int = 0, limit: int = 100) -> List[Ticket]:
    return session.exec(
        select(Ticket)
        .where(Ticket.assigned_to_id == support_id)
        .offset(skip)
        .limit(limit)
    ).all()

def get_all_tickets(
    session: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at"
) -> List[Ticket]:
    query = select(Ticket)
    if status:
        query = query.where(Ticket.status == status)
    if priority:
        query = query.where(Ticket.priority == priority)
    if sort_by == "created_at":
        query = query.order_by(Ticket.created_at.desc())
    query = query.offset(skip).limit(limit)
    return session.exec(query).all()

def update_ticket(session: Session, ticket_id: str, ticket_update: TicketUpdate) -> Optional[Ticket]:
    ticket = get_ticket_by_id(session, ticket_id)
    if not ticket:
        return None
    if ticket_update.title:
        ticket.title = ticket_update.title
    if ticket_update.description:
        ticket.description = ticket_update.description
    if ticket_update.status:
        ticket.status = ticket_update.status
    if ticket_update.priority:
        ticket.priority = ticket_update.priority
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket