from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional, Literal


class HabitBase(BaseModel):
    title: str
    description: Optional[str] = None
    activity_type: Literal["correr", "caminar", "pasos"]
    is_public: bool = True


class HabitCreate(HabitBase):
    @validator("activity_type")
    def validate_activity_type(cls, v):
        if v not in ["correr", "caminar", "pasos"]:
            raise ValueError('activity_type debe ser "correr", "caminar" o "pasos"')
        return v


class HabitUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    activity_type: Optional[Literal["correr", "caminar", "pasos"]]
    is_public: Optional[bool]


class HabitResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    activity_type: str
    is_public: bool
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
