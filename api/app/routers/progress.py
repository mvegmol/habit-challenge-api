from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Union
import logging

from ..db import get_db
from ..schemas.progress import (
    ProgressCreate,
    ProgressResponse,
    ProgressSummaryRunning,
    ProgressSummarySteps,
)
from ..crud import progress as progress_crud, habit as habit_crud
from ..utils.dependencies import get_current_active_user
from ..models.user import User
from ..external_services.weather import get_weather
from ..config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/", response_model=ProgressResponse)
async def create_progress_entry(
    progress: ProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    # Obtener el hábito para validar el tipo de actividad
    habit = habit_crud.get_habit(db, progress.habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")

    # Verificar que el usuario sea el propietario del hábito
    if habit.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para agregar progreso a este hábito",
        )

    # Validar campos según el tipo de actividad
    progress_data = progress.dict()

    if habit.activity_type in ["correr", "caminar"]:
        # Validar campos requeridos para correr/caminar
        if (
            not progress.distance_km
            or not progress.duration_minutes
            or not progress.city
        ):
            raise HTTPException(
                status_code=400,
                detail="Para actividades de correr/caminar se requieren: distance_km, duration_minutes y city",
            )

        # Calcular pace
        pace = progress.duration_minutes / progress.distance_km
        progress_data["pace"] = pace

        # Obtener datos del clima
        logger.info(f"Intentando obtener clima para ciudad: {progress.city}")
        logger.info(f"API Key disponible: {bool(settings.openweather_api_key)}")
        logger.info(
            f"API Key valor: {settings.openweather_api_key[:8] if settings.openweather_api_key else 'None'}..."
        )

        weather_data = await get_weather(progress.city, settings.openweather_api_key)
        logger.info(f"Datos del clima recibidos: {weather_data}")

        if weather_data:
            progress_data.update(
                {
                    "weather_temperature": weather_data["temperature"],
                    "weather_description": weather_data["description"],
                    "weather_humidity": weather_data["humidity"],
                    "wind_speed": weather_data["wind_speed"],
                }
            )
            logger.info("Datos del clima agregados al progreso")
        else:
            logger.warning(f"No se pudo obtener datos del clima para {progress.city}")
            logger.info("Estableciendo valores de clima como null")

        # Limpiar campos no aplicables
        progress_data["steps"] = None

    elif habit.activity_type == "pasos":
        # Validar campos requeridos para pasos
        if not progress.steps:
            raise HTTPException(
                status_code=400,
                detail="Para actividad de pasos se requiere el campo: steps",
            )

        # Limpiar campos no aplicables
        progress_data.update(
            {
                "distance_km": None,
                "duration_minutes": None,
                "pace": None,
                "city": None,
                "weather_temperature": None,
                "weather_description": None,
                "weather_humidity": None,
                "wind_speed": None,
            }
        )

    return progress_crud.create_progress(db, progress_data, user_id=current_user.id)


@router.get("/summary/")
def get_progress_summary(
    days: int = Query(..., ge=1, le=365, description="Número de días para el resumen"),
    activity_type: str = Query(
        ..., regex="^(correr|caminar|pasos)$", description="Tipo de actividad"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Union[ProgressSummaryRunning, ProgressSummarySteps]:
    """
    Obtiene un resumen del progreso del usuario para un tipo de actividad específico
    en los últimos X días.
    """
    if activity_type in ["correr", "caminar"]:
        summary = progress_crud.get_progress_summary_running(
            db, current_user.id, activity_type, days
        )
        return ProgressSummaryRunning(**summary)
    else:  # pasos
        summary = progress_crud.get_progress_summary_steps(db, current_user.id, days)
        return ProgressSummarySteps(**summary)


@router.get("/habit/{habit_id}", response_model=List[ProgressResponse])
def get_progress_for_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return progress_crud.get_progress_by_habit(db, habit_id)


@router.get("/me", response_model=List[ProgressResponse])
def get_my_progress(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    return progress_crud.get_progress_by_user(db, user_id=current_user.id)
