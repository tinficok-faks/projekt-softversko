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

def update_ticket_status(session: Session, ticket_id: str, status: str) -> Optional[Ticket]:
    ticket = get_ticket_by_id(session, ticket_id)
    if ticket:
        ticket.status = status
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
    return ticket

def update_ticket_priority(session: Session, ticket_id: str, priority: str) -> Optional[Ticket]:
    ticket = get_ticket_by_id(session, ticket_id)
    if ticket:
        ticket.priority = priority
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
    return ticket

def assign_ticket(session: Session, ticket_id: str, support_id: str) -> Optional[Ticket]:
    ticket = get_ticket_by_id(session, ticket_id)
    if not ticket:
        return None
    ticket.assigned_to_id = support_id
    ticket.status = "assigned"
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

def delete_ticket(session: Session, ticket_id: str) -> bool:
    ticket = get_ticket_by_id(session, ticket_id)
    if ticket:
        session.delete(ticket)
        session.commit()
        return True
    return False

def get_ticket_statistics(session: Session) -> dict:
    total = len(session.exec(select(Ticket)).all())
    assigned = len(session.exec(select(Ticket).where(Ticket.status == "assigned")).all())
    solved = len(session.exec(select(Ticket).where(Ticket.status == "solved")).all())
    new = len(session.exec(select(Ticket).where(Ticket.status == "new")).all())
    seen = len(session.exec(select(Ticket).where(Ticket.status == "seen")).all())
    urgent = len(session.exec(select(Ticket).where(Ticket.priority == "urgent")).all())
    
    return {
        "total_tickets": total,
        "new_tickets": new,
        "seen_tickets": seen,
        "assigned_tickets": assigned,
        "solved_tickets": solved,
        "urgent_tickets": urgent,
        "avg_time_to_solve": None
    }