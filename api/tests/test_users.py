import pytest
from api.app.models.user import User

def test_read_users(authorized_client, db, test_user):
    response = authorized_client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["email"] == test_user.email

def test_get_current_user_profile(authorized_client, test_user):
    response = authorized_client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username

def test_update_current_user_profile(authorized_client, test_user):
    response = authorized_client.put(
        "/users/me",
        json={
            "username": "updated_username",
            "email": "updated@example.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updated_username"
    assert data["email"] == "updated@example.com"

def test_delete_current_user_account(authorized_client, db, test_user):
    response = authorized_client.delete("/users/me")
    assert response.status_code == 204

    # Verificar que el usuario fue eliminado
    deleted_user = db.query(User).filter(User.id == test_user.id).first()
    assert deleted_user is None

def test_get_specific_user(authorized_client, test_user):
    response = authorized_client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email

def test_update_other_user_forbidden(authorized_client, db):
    # Crear otro usuario
    other_user = User(
        email="other@example.com",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LHKj4nY9GHNM10cui",
        username="other_user",
        is_active=True
    )
    db.add(other_user)
    db.commit()
    db.refresh(other_user)

    response = authorized_client.put(
        f"/users/{other_user.id}",
        json={
            "username": "hacked_username",
            "email": "hacked@example.com"
        }
    )
    assert response.status_code == 403

def test_delete_other_user_forbidden(authorized_client, db):
    # Crear otro usuario
    other_user = User(
        email="other@example.com",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LHKj4nY9GHNM10cui",
        username="other_user",
        is_active=True
    )
    db.add(other_user)
    db.commit()
    db.refresh(other_user)

    response = authorized_client.delete(f"/users/{other_user.id}")
    assert response.status_code == 403
