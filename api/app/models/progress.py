from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    # e.g., number of steps, minutes, etc.
    value = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    habit_id = Column(Integer, ForeignKey("habits.id"))

    user = relationship("User", back_populates="progresses")
    habit = relationship("Habit", back_populates="progresses")
