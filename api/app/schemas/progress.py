from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import Optional


class ProgressBase(BaseModel):
    date: date
    # Campos para actividades físicas
    distance_km: Optional[float] = None
    duration_minutes: Optional[float] = None
    steps: Optional[int] = None
    city: Optional[str] = None


class ProgressCreate(ProgressBase):
    habit_id: int

    @validator("distance_km")
    def validate_distance(cls, v):
        if v is not None and v <= 0:
            raise ValueError("distance_km debe ser mayor que 0")
        return v

    @validator("duration_minutes")
    def validate_duration(cls, v):
        if v is not None and v <= 0:
            raise ValueError("duration_minutes debe ser mayor que 0")
        return v

    @validator("steps")
    def validate_steps(cls, v):
        if v is not None and v <= 0:
            raise ValueError("steps debe ser mayor que 0")
        return v


class ProgressResponse(BaseModel):
    id: int
    date: date
    distance_km: Optional[float] = None
    duration_minutes: Optional[float] = None
    pace: Optional[float] = None
    steps: Optional[int] = None
    city: Optional[str] = None
    weather_temperature: Optional[float] = None
    weather_description: Optional[str] = None
    weather_humidity: Optional[int] = None
    wind_speed: Optional[float] = None
    user_id: int
    habit_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProgressSummaryRunning(BaseModel):
    activity_type: str
    days: int
    total_distance_km: float
    total_duration_minutes: float
    average_pace: float


class ProgressSummarySteps(BaseModel):
    activity_type: str
    days: int
    total_steps: int
