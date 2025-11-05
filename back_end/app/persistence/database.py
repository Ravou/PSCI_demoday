import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv


# [translate:Charger les variables d'environnement depuis .env]
load_dotenv()


# [translate:Récupérer l'URL de la base depuis l'environnement]
DATABASE_URL = os.getenv("DATABASE_URL")


# [translate:Créer l'engine SQLAlchemy]
engine = create_engine(DATABASE_URL, echo=True)


# [translate:Factory pour les sessions]
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# [translate:Base pour tous les modèles]
Base = declarative_base()

