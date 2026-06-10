from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Création du dossier "instance" s’il n’existe pas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

# Fichier SQLite
DATABASE_PATH = os.path.join(INSTANCE_DIR, "cosmetiq.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Connexion SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
