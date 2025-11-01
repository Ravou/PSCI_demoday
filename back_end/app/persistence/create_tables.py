from app.persistence.database import Base, engine
from app.models.user import User
from app.models.audit import Audit

print("🧱 Creating PostgreSQL tables for PSCI...")

# Génère toutes les tables à partir des modèles SQLAlchemy
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully in PSCI database.")