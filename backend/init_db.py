from sqlmodel import Session, create_engine, select
from app.config import settings
from app.models import User
from app.database import create_db_and_tables
from app.crud.user import create_user, update_user_role, get_user_by_email
from app.models import UserCreate

def init_sample_data():
    engine = create_engine(
        settings.DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    )
    create_db_and_tables()
    
    with Session(engine) as session:
        admin_email = "admin@helpdesk.local"
        if not get_user_by_email(session, admin_email):
            admin_user = User(
                username="admin",
                email=admin_email,
                password="admin123", 
                role="admin"
            )
            admin = create_user(session, admin_user)
            update_user_role(session, admin.id, "admin")
            print(f" Admin user created: {admin.username}")
        else:
            print(f" Admin user already exists: {admin_email}")
        
        for i in range(3):
            support_email = f"support{i+1}@helpdesk.local"
            if not get_user_by_email(session, support_email):
                support_user = UserCreate(
                    username=f"support{i+1}",
                    email=support_email,
                    password="support123",
                    role="support"
                )
                support = create_user(session, support_user)
                update_user_role(session, support.id, "support")
                print(f" Support user created: {support_user.username}")
            else:
                print(f" Support user already exists: {support_email}")
        
        for i in range(3):
            user_email = f"user{i+1}@example.com"
            if not get_user_by_email(session, user_email):
                user = UserCreate(
                    username=f"user{i+1}",
                    email=user_email,
                    password="user123",
                    role="user"
                )
                create_user(session, user)
                print(f" User created: {user.username}")
            else:
                print(f" User already exists: {user_email}")
        
        session.commit()


if __name__ == "__main__":
    init_sample_data()
