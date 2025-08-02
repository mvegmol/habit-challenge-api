from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional, Dict, Any
from datetime import date, timedelta
from ..models.progress import Progress
from ..models.habit import Habit
from ..schemas.progress import ProgressCreate


def create_progress(
    db: Session, progress_data: Dict[str, Any], user_id: int
) -> Progress:
    """
    Crea un nuevo registro de progreso con todos los campos disponibles.
    """
    db_progress = Progress(user_id=user_id, **progress_data)
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress


def get_progress_by_habit(db: Session, habit_id: int) -> List[Progress]:
    return db.query(Progress).filter(Progress.habit_id == habit_id).all()


def get_progress_by_user(db: Session, user_id: int) -> List[Progress]:
    return db.query(Progress).filter(Progress.user_id == user_id).all()


def get_progress_summary_running(
    db: Session, user_id: int, activity_type: str, days: int
) -> Optional[Dict[str, Any]]:
    """
    Obtiene resumen de progreso para actividades de correr/caminar.
    """
    start_date = date.today() - timedelta(days=days - 1)

    result = (
        db.query(
            func.sum(Progress.distance_km).label("total_distance"),
            func.sum(Progress.duration_minutes).label("total_duration"),
            func.count(Progress.id).label("count"),
        )
        .join(Habit)
        .filter(
            and_(
                Progress.user_id == user_id,
                Habit.activity_type == activity_type,
                Progress.date >= start_date,
                Progress.distance_km.isnot(None),
                Progress.duration_minutes.isnot(None),
            )
        )
        .first()
    )

    if not result or not result.total_distance:
        return {
            "activity_type": activity_type,
            "days": days,
            "total_distance_km": 0.0,
            "total_duration_minutes": 0.0,
            "average_pace": 0.0,
        }

    average_pace = (
        result.total_duration / result.total_distance
        if result.total_distance > 0
        else 0
    )

    return {
        "activity_type": activity_type,
        "days": days,
        "total_distance_km": float(result.total_distance),
        "total_duration_minutes": float(result.total_duration),
        "average_pace": float(average_pace),
    }


def get_progress_summary_steps(db: Session, user_id: int, days: int) -> Dict[str, Any]:
    """
    Obtiene resumen de progreso para actividad de pasos.
    """
    start_date = date.today() - timedelta(days=days - 1)

    result = (
        db.query(func.sum(Progress.steps).label("total_steps"))
        .join(Habit)
        .filter(
            and_(
                Progress.user_id == user_id,
                Habit.activity_type == "pasos",
                Progress.date >= start_date,
                Progress.steps.isnot(None),
            )
        )
        .first()
    )

    total_steps = result.total_steps if result and result.total_steps else 0

    return {"activity_type": "pasos", "days": days, "total_steps": int(total_steps)}
