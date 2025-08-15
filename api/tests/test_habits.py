import pytest
from api.app.models.habit import Habit

def test_create_habit(authorized_client, db, test_user):
    # Asegurarse de que el usuario esté adjunto a la sesión
    db.add(test_user)
    db.commit()
    response = authorized_client.post(
        "/habits/",
        json={
            "title": "Running",
            "description": "Daily running habit",
            "activity_type": "correr",
            "is_public": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Running"
    assert "owner_id" in data

def test_get_user_habits(authorized_client, db, test_user):
    # Crear algunos hábitos de prueba
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

    response = authorized_client.get("/habits/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Running"
    assert data[1]["title"] == "Walking"

def test_get_habit_by_id(authorized_client, db, test_user):
    # Crear un hábito de prueba
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

    response = authorized_client.get(f"/habits/{habit.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Running"
    assert data["id"] == habit.id

def test_update_habit(authorized_client, db, test_user):
    # Crear un hábito de prueba
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

    response = authorized_client.put(
        f"/habits/{habit.id}",
        json={
            "title": "Updated Running",
            "description": "Updated description",
            "activity_type": "correr",
            "is_public": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Running"

def test_delete_habit(authorized_client, db, test_user):
    # Crear un hábito de prueba
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

    response = authorized_client.delete(f"/habits/{habit.id}")
    assert response.status_code == 204

    # Verificar que el hábito ya no existe
    response = authorized_client.get(f"/habits/{habit.id}")
    assert response.status_code == 404
