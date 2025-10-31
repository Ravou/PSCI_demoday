from app.persistence.database import engine
from app.models.user import User
from app.models.audit import Audit

# ⚠️ ATTENTION : les données de ces tables seront supprimées !
tables_to_drop = [Audit.__table__, User.__table__]

print("Suppression des tables sélectionnées...")
for table in tables_to_drop:
    table.drop(engine, checkfirst=True)  # checkfirst=True évite l'erreur si la table n'existe pas

print("✅ Les tables 'users' et 'audits' ont été supprimées avec succès.")

