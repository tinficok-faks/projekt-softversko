from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Index
import uuid

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password: str
    role: str = Field(default="user")
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    __tablename__ = "user"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(SQLModel):
    username: str
    email: str
    password: str

class UserRead(SQLModel):
    id: str
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class TicketBase(SQLModel):
    title: str = Field(index=True)
    description: str
    status: str = Field(default="new")
    priority: str = Field(default="medium")

class Ticket(TicketBase, table=True):
    __tablename__ = "ticket"
    __table_args__ = (
        Index('idx_status_priority', 'status', 'priority'),
        Index('idx_created_at', 'created_at'),
        Index('idx_assigned_to', 'assigned_to_id'),
    )
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by_id: str = Field(foreign_key="user.id", index=True)
    assigned_to_id: Optional[str] = Field(default=None, foreign_key="user.id", index=True)
    created_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "Ticket.created_by_id",
            "primaryjoin": "Ticket.created_by_id == User.id"
        }
    )
    assigned_to_support: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "Ticket.assigned_to_id",
            "primaryjoin": "Ticket.assigned_to_id == User.id"
        }
    )
    attachments: List["Attachment"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}
    )

class TicketCreate(SQLModel):
    title: str
    description: str
    priority: Optional[str] = "medium"

class TicketRead(SQLModel):
    id: str
    title: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    created_by_id: str
    assigned_to_id: Optional[str] = None

class TicketUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class TicketAssign(SQLModel):
    support_user_id: str

class AttachmentBase(SQLModel):
    file_name: str
    file_path: str

class Attachment(AttachmentBase, table=True):
    __tablename__ = "attachment"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    ticket_id: str = Field(foreign_key="ticket.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ticket: Optional["Ticket"] = Relationship(
        sa_relationship_kwargs={"overlaps": "attachments"}
    )

class AttachmentRead(SQLModel):
    id: str
    file_name: str
    file_path: str
    ticket_id: str
    created_at: datetime