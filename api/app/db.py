from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Crear el engine
engine = create_engine(settings.database_url, echo=settings.debug)

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


# Dependencia para inyectar en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
