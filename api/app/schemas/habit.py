from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class HabitBase(BaseModel):

    title: str
    description: Optional[str] = None
    frequency: str = "Daily"
    is_public: bool = True


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    frequency: Optional[str]
    is_public: Optional[bool]


class HabitResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    frequency: str
    is_public: bool
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True
