from sqlmodel import Session, select
from app.models import User, UserCreate, UserRead
from app.security import hash_password, verify_password

def create_user(session: Session, user_create: UserCreate) -> User:
    user = User(
        username=user_create.username,
        email=user_create.email,
        password=hash_password(user_create.password),
        role="user"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_id(session: Session, user_id: str) -> User:
    return session.exec(select(User).where(User.id == user_id)).first()

def get_user_by_username(session: Session, username: str) -> User:
    return session.exec(select(User).where(User.username == username)).first()

def get_user_by_email(session: Session, email: str) -> User:
    return session.exec(select(User).where(User.email == email)).first()

def get_users_by_role(session: Session, role: str):
    return session.exec(select(User).where(User.role == role)).all()

def authenticate_user(session: Session, username: str, password: str) -> User:
    user = get_user_by_username(session, username)
    if not user or not verify_password(password, user.password):
        return None
    return user