from fastapi import FastAPI
from .db import engine, Base

# Importar modelos ANTES de crear las tablas (necesario para que SQLAlchemy los registre)
from .models.user import User
from .models.habit import Habit
from .models.progress import Progress

# Importar routers
from .routers import auth, users, habits, progress

app = FastAPI(
    title="Habit Challenge API",
    description="API para gestión de hábitos y seguimiento de progreso",
    version="1.0.0",
)

# Incluir routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(habits.router)
app.include_router(progress.router)
# Crear las tablas DESPUÉS de importar todos los modelos
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Habit Challenge API - Running!"}
