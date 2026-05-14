from sqlmodel import Session, create_engine, select
from app.config import settings
from app.models import User
from app.database import create_db_and_tables


def init_sample_data():
    engine = create_engine(
        settings.DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    )
    create_db_and_tables()
    
    with Session(engine) as session:
        admin_email = "admin@helpdesk.local"
        admin = session.exec(select(User).where(User.email == admin_email)).first()
        if not admin:
            admin_user = User(
                username="admin",
                email=admin_email,
                password="admin123", 
                role="admin"
            )
            session.add(admin_user)
            print(f" Admin user created: {admin_user.username}")
        else:
            print(f" Admin user already exists: {admin_email}")
        
        for i in range(3):
            support_email = f"support{i+1}@helpdesk.local"
            support = session.exec(select(User).where(User.email == support_email)).first()
            if not support:
                support_user = User(
                    username=f"support{i+1}",
                    email=support_email,
                    password="support123",
                    role="support"
                )
                session.add(support_user)
                print(f" Support user created: {support_user.username}")
            else:
                print(f" Support user already exists: {support_email}")
        
        for i in range(3):
            user_email = f"user{i+1}@example.com"
            user_db = session.exec(select(User).where(User.email == user_email)).first()
            if not user_db:
                user = User(
                    username=f"user{i+1}",
                    email=user_email,
                    password="user123",
                    role="user"
                )
                session.add(user)
                print(f" User created: {user.username}")
            else:
                print(f" User already exists: {user_email}")
        
        session.commit()


if __name__ == "__main__":
    init_sample_data()
