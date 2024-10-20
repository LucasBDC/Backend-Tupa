from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database.db import get_db
from app.domain.models.user import UserCreate, UserRead
from app.domain.services.user_service import UserService

router = APIRouter()

@router.post("/users", response_model=UserRead)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user_data)

@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_user_by_id(user_id)

@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.update_user(user_id, user_data)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.delete_user(user_id)
