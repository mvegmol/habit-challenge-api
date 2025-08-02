from fastapi import FastAPI
from .db import engine, Base

# Importar modelos
from .models import user, habit, progress

app = FastAPI()

# Crear las tablas si no existen

Base.metadata.create_all(bind=engine)
