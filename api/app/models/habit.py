from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db import Base


class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    activity_type = Column(String, nullable=False)  # "correr", "caminar", "pasos"
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="habits")
    progresses = relationship("Progress", back_populates="habit")
