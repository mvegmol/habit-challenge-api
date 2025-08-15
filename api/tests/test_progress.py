import pytest
from datetime import datetime
from api.app.models.habit import Habit
from api.app.models.progress import Progress
import json

def test_create_progress_running(authorized_client, db, test_user):
    # Crear un hábito de tipo correr
    habit = Habit(
        title="Running",
        description="Daily running",
        activity_type="correr",
        is_public=True,
        owner_id=test_user.id
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)

    response = authorized_client.post(
        "/progress/",
        json={
            "habit_id": habit.id,
            "date": datetime.now().date().isoformat(),
            "distance_km": 5.0,
            "duration_minutes": 30,
            "city": "Madrid"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["distance_km"] == 5.0
    assert data["duration_minutes"] == 30
    assert data["pace"] == 6.0  # 30 minutos / 5 km

def test_create_progress_steps(authorized_client, db, test_user):
    # Crear un hábito de tipo pasos
    habit = Habit(
        title="Daily Steps",
        description="Daily steps goal",
        activity_type="pasos",
        is_public=True,
        owner_id=test_user.id
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)

    response = authorized_client.post(
        "/progress/",
        json={
            "habit_id": habit.id,
            "date": datetime.now().date().isoformat(),
            "steps": 8000
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["steps"] == 8000
    assert data["distance_km"] is None
    assert data["duration_minutes"] is None

def test_get_progress_summary_running(authorized_client, db, test_user):
    # Crear un hábito y algunos registros de progreso
    habit = Habit(
        title="Running",
        description="Daily running",
        activity_type="correr",
        is_public=True,
        owner_id=test_user.id
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)

    # Crear algunos registros de progreso con valores de pace
    progresses = [
        Progress(
            habit_id=habit.id,
            user_id=test_user.id,
            date=datetime.now().date(),
            distance_km=5.0,
            duration_minutes=30,
            pace=6.0,  # 30 minutos / 5 km = 6.0 min/km
            city="Madrid"
        ),
        Progress(
            habit_id=habit.id,
            user_id=test_user.id,
            date=datetime.now().date(),
            distance_km=6.0,
            duration_minutes=35,
            pace=5.83,  # 35 minutos / 6 km ≈ 5.83 min/km
            city="Madrid"
        )
    ]
    db.add_all(progresses)
    db.commit()

    response = authorized_client.get("/progress/summary/?days=7&activity_type=correr")
    assert response.status_code == 200
    data = response.json()
    assert "total_distance_km" in data
    assert "total_duration_minutes" in data
    assert "average_pace" in data

def test_get_progress_by_habit(authorized_client, db, test_user):
    # Crear un hábito y algunos registros de progreso
    habit = Habit(
        title="Running",
        description="Daily running",
        activity_type="correr",
        is_public=True,
        owner_id=test_user.id
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)

    progress = Progress(
        habit_id=habit.id,
        user_id=test_user.id,
        date=datetime.now().date(),
        distance_km=5.0,
        duration_minutes=30,
        pace=6.0,  # 30 minutos / 5 km = 6.0 min/km
        city="Madrid"
    )
    db.add(progress)
    db.commit()

    response = authorized_client.get(f"/progress/habit/{habit.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["distance_km"] == 5.0

def test_get_my_progress(authorized_client, db, test_user):
    # Crear múltiples hábitos y progreso
    habits = [
        Habit(
            title="Running",
            description="Daily running",
            activity_type="correr",
            is_public=True,
            owner_id=test_user.id
        ),
        Habit(
            title="Walking",
            description="Daily walking",
            activity_type="caminar",
            is_public=True,
            owner_id=test_user.id
        )
    ]
    db.add_all(habits)
    db.commit()
    for habit in habits:
        db.refresh(habit)

    # Crear progreso para ambos hábitos
    progresses = [
        Progress(
            habit_id=habits[0].id,
            user_id=test_user.id,
            date=datetime.now().date(),
            distance_km=5.0,
            duration_minutes=30,
            pace=6.0,  # 30 minutos / 5 km = 6.0 min/km
            city="Madrid"
        ),
        Progress(
            habit_id=habits[1].id,
            user_id=test_user.id,
            date=datetime.now().date(),
            distance_km=3.0,
            duration_minutes=45,
            pace=15.0,  # 45 minutos / 3 km = 15.0 min/km
            city="Madrid"
        )
    ]
    db.add_all(progresses)
    db.commit()

    response = authorized_client.get("/progress/me")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(p["distance_km"] == 5.0 for p in data)
    assert any(p["distance_km"] == 3.0 for p in data)
