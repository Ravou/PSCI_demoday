"""
Script d'initialisation de la base de données
Compatible avec authentification PostgreSQL peer
"""
import sys
import os

# Ajouter le répertoire du projet au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importer Flask et SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuration de la base de données (authentification peer)
DATABASE_URL = 'postgresql:///psci_db'

# Créer l'application Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser SQLAlchemy
db = SQLAlchemy(app)

# IMPORTANT: Importer les modèles APRÈS avoir initialisé db
from app.models.user import User
from app.models.consent_log import ConsentLog
from app.models.audit import Audit

def init_database():
    """Initialise la base de données avec les tables"""
   
    with app.app_context():
        print("\n" + "="*50)
        print("INITIALISATION DE LA BASE DE DONNÉES")
        print("="*50 + "\n")
        
        print("📌 Connexion à:", DATABASE_URL)
        
        try:
            print("\n🗑️  Suppression des tables existantes...")
            db.drop_all()
            
            print("✨ Création des nouvelles tables...")
            db.create_all()
            
            # Vérifier les tables créées
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if not tables:
                print("\n❌ ERREUR: Aucune table créée!")
                print("Les modèles n'ont pas été importés correctement.")
                return False
            
            print(f"\n✅ {len(tables)} table(s) créée(s) avec succès!\n")
            
            # Afficher la structure de chaque table
            for table in tables:
                print(f"📋 Table: {table}")
                columns = inspector.get_columns(table)
                
                for i, col in enumerate(columns):
                    prefix = "  └─" if i == len(columns) - 1 else "  ├─"
                    nullable = "NULL" if col.get('nullable') else "NOT NULL"
                    print(f"{prefix} {col['name']}: {col['type']} ({nullable})")
                print()
            
            print("="*50)
            print("✅ INITIALISATION TERMINÉE")
            print("="*50 + "\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERREUR lors de l'initialisation:")
            print(f"   {type(e).__name__}: {e}")
            print("\n💡 Vérifiez les identifiants PostgreSQL dans DATABASE_URL")
            return False

if __name__ == '__main__':
    success = init_database()
    if not success:
        sys.exit(1)
