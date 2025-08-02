from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from ..schemas.habit import HabitCreate, HabitResponse, HabitUpdate
from ..crud import habit as habit_crud
from ..utils.dependencies import get_current_active_user
from ..models.user import User


router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("/", response_model=HabitResponse)
def create_user_habit(
    habit: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return habit_crud.create_habit(db=db, habit=habit, owner_id=current_user.id)


@router.get("/", response_model=List[HabitResponse])
def list_user_habits(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    return habit_crud.get_habits_by_user(db, owner_id=current_user.id)


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit_by_id(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_habit = habit_crud.get_habit(db, habit_id)
    if not db_habit or db_habit.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Habit not found")
    return db_habit


@router.put("/{habit_id}", response_model=HabitResponse)
def update_user_habit(
    habit_id: int,
    habit_update: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_habit = habit_crud.get_habit(db, habit_id)
    if not db_habit or db_habit.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit_crud.update_habit(db, habit_id, habit_update)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_habit = habit_crud.get_habit(db, habit_id)
    if not db_habit or db_habit.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Habit not found")
    habit_crud.delete_habit(db, habit_id)
