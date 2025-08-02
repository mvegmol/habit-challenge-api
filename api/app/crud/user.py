from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..utils.auth import get_password_hash
from typing import Optional


# Obtener usuario por ID
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


#  Obtener usuario por email
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


# Obtener lista de usuarios con paginación
def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(User).offset(skip).limit(limit).all()


# Crear un nuevo usuario
def create_user(db: Session, user: UserCreate) -> User:
    """"""
    # Hash de la contraseña
    hashed_password = get_password_hash(user.password)

    # Crear instancia del usuario
    db_user = User(
        email=user.email, hashed_password=hashed_password, full_name=user.full_name
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this email already exists")


# Actualizar un usuario existente
def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:

    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.dict(exclude_unset=True)

    # Si se está actualizando la contraseña, hashearla
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# Eliminar un usuario
def delete_user(db: Session, user_id: int) -> bool:

    db_user = get_user(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True


# Autenticar usuario con email y contraseña
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:

    from ..utils.auth import verify_password

    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
