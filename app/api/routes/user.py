from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database.db import get_db
from app.domain.models.user import UserCreate, UserRead
from app.domain.services.user_service import UserService
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/users", response_model=UserRead)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user_data)

@router.get("/me", response_model=UserRead)
def get_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_service = UserService(db)
    current_user = user_service.get_current_user(db, token)
    return user_service.get_user(current_user)

@router.put("/me", response_model=UserRead)
def update_user(user_data: UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_service = UserService(db)
    current_user = user_service.get_current_user(db, token)
    return user_service.update_user(user_data, current_user)

@router.delete("/me")
def delete_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_service = UserService(db)
    current_user = user_service.get_current_user(db, token)
    return user_service.delete_user(current_user)

@router.patch("/me/deactivate")
def deactivate_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_service = UserService(db)
    current_user = user_service.get_current_user(db, token)
    return user_service.deactivate_user(current_user)

@router.patch("/users/{user_id}/activate")
def activate_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.activate_user(user_id)
