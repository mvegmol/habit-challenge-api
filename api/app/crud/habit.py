from sqlalchemy.orm import Session
from ..models.habit import Habit
from ..schemas.habit import HabitCreate, HabitUpdate
from typing import List, Optional


def create_habit(db: Session, habit: HabitCreate, owner_id: int) -> Habit:
    db_habit = Habit(**habit.dict(), owner_id=owner_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


def get_habit(db: Session, habit_id: int) -> Optional[Habit]:
    return db.query(Habit).filter(Habit.id == habit_id).first()


def get_habits_by_user(db: Session, owner_id: int) -> List[Habit]:
    return db.query(Habit).filter(Habit.owner_id == owner_id).all()


def update_habit(
    db: Session, habit_id: int, habit_data: HabitUpdate
) -> Optional[Habit]:
    db_habit = get_habit(db, habit_id)

    if not db_habit:
        return None

    for key, value in habit_data.dict(exclude_unset=True).items():
        setattr(db_habit, key, value)

    db.commit()
    db.refresh(db_habit)
    return db_habit


def delete_habit(db: Session, habit_id: int) -> bool:
    db_habit = get_habit(db, habit_id)
    if not db_habit:
        return False
    db.delete(db_habit)
    db.commit()
    return True
