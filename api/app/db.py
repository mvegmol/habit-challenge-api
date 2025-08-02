from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de conexion postgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://miguel:123@localhost:5432/habit-challenge")

# Crear el engine
engine = create_engine(DATABASE_URL, echo=True)

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para inyectar en rutas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
