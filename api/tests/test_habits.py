import pytest
from api.app.models.habit import Habit

def test_create_habit(authorized_client, test_user):
    response = authorized_client.post(
        "/habits/",
        json={
            "name": "Running",
            "description": "Daily running habit",
            "activity_type": "correr",
            "frequency": "diario",
            "goal": 5.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Running"
    assert data["owner_id"] == test_user.id

def test_get_user_habits(authorized_client, db, test_user):
    # Crear algunos hábitos de prueba
    habits = [
        Habit(
            name="Running",
            description="Daily running",
            activity_type="correr",
            frequency="diario",
            goal=5.0,
            owner_id=test_user.id
        ),
        Habit(
            name="Walking",
            description="Daily walking",
            activity_type="caminar",
            frequency="diario",
            goal=3.0,
            owner_id=test_user.id
        )
    ]
    db.add_all(habits)
    db.commit()

    response = authorized_client.get("/habits/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Running"
    assert data[1]["name"] == "Walking"

def test_get_habit_by_id(authorized_client, db, test_user):
    # Crear un hábito de prueba
    habit = Habit(
        name="Running",
        description="Daily running",
        activity_type="correr",
        frequency="diario",
        goal=5.0,
        owner_id=test_user.id
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)

    response = authorized_client.get(f"/habits/{habit.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Running"
    assert data["id"] == habit.id

def test_update_habit(authorized_client, db, test_user):
    # Crear un hábito de prueba
    habit = Habit(
        name="Running",
        description="Daily running",
        activity_type="correr",
        frequency="diario",
        goal=5.0,
        owner_id=test_user.id
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)

    response = authorized_client.put(
        f"/habits/{habit.id}",
        json={
            "name": "Updated Running",
            "description": "Updated description",
            "goal": 6.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Running"
    assert data["goal"] == 6.0

def test_delete_habit(authorized_client, db, test_user):
    # Crear un hábito de prueba
    habit = Habit(
        name="Running",
        description="Daily running",
        activity_type="correr",
        frequency="diario",
        goal=5.0,
        owner_id=test_user.id
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)

    response = authorized_client.delete(f"/habits/{habit.id}")
    assert response.status_code == 204

    # Verificar que el hábito ya no existe
    response = authorized_client.get(f"/habits/{habit.id}")
    assert response.status_code == 404
