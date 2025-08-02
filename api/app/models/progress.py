from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    # Campos para actividades físicas
    distance_km = Column(Float, nullable=True)  # Solo para correr/caminar
    duration_minutes = Column(Float, nullable=True)  # Solo para correr/caminar
    pace = Column(Float, nullable=True)  # Calculado como duration_minutes / distance_km
    steps = Column(Integer, nullable=True)  # Solo para tipo "pasos"
    # Campos de clima
    city = Column(String, nullable=True)
    weather_temperature = Column(Float, nullable=True)
    weather_description = Column(String, nullable=True)
    weather_humidity = Column(Integer, nullable=True)
    wind_speed = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    habit_id = Column(Integer, ForeignKey("habits.id"))

    user = relationship("User", back_populates="progresses")
    habit = relationship("Habit", back_populates="progresses")
