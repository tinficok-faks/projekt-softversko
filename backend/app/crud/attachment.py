from typing import Optional, List
from sqlmodel import Session, select
from app.models import Attachment, AttachmentRead

def create_attachment(session: Session, file_name: str, file_path: str, ticket_id: str) -> Attachment:
    attachment = Attachment(
        file_name=file_name,
        file_path=file_path,
        ticket_id=ticket_id
    )
    session.add(attachment)
    session.commit()
    session.refresh(attachment)
    return attachment

def get_attachment_by_id(session: Session, attachment_id: str) -> Optional[Attachment]:
    return session.exec(select(Attachment).where(Attachment.id == attachment_id)).first()

def get_ticket_attachments(session: Session, ticket_id: str) -> List[Attachment]:
    return session.exec(select(Attachment).where(Attachment.ticket_id == ticket_id)).all()

def delete_attachment(session: Session, attachment_id: str) -> bool:
    attachment = get_attachment_by_id(session, attachment_id)
    if attachment:
        session.delete(attachment)
        session.commit()
        return True
    return False