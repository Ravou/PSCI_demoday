# app/persistence/seed_data.py
from app.persistence.database import SessionLocal
from app.models.user import User

def seed_initial_data():
    session = SessionLocal()
    try:
        # Crée un admin si non existant
        if not session.query(User).filter_by(email="admin@psci.io").first():
            admin = User(
                name="Admin PSCI",
                email="admin@psci.io",
                password="admin1234",
                consent_ip="127.0.0.1",
                is_admin=True
            )
            session.add(admin)
            session.commit()
            print(" Admin user created successfully.")
        else:
            print(" Admin user already exists.")
    finally:
        session.close()

if __name__ == "__main__":
    seed_initial_data()