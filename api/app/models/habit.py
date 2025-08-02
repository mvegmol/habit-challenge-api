from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db import Base


class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    frequency = Column(String, default="daily")
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("user", back_populates="habits")
    progresses = relationship("Progress", back_populates="habit")
