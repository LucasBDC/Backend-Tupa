from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.db import get_db
from app.domain.models.category import CategoryCreate, CategoryRead
from app.domain.services.category_service import CategoryService
from app.domain.services.user_service import get_current_user
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/categories", response_model=CategoryRead)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    category_service = CategoryService(db)
    current_user = get_current_user(db, token)
    return category_service.create_category(current_user, category_data)

@router.get("/categories", response_model=list[CategoryRead])
def get_user_categories(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    category_service = CategoryService(db)
    current_user = get_current_user(db, token)
    return category_service.get_user_categories(current_user)

@router.get("/categories/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    category_service = CategoryService(db)
    current_user = get_current_user(db, token)
    return category_service.get_category_by_id(category_id, current_user)

@router.put("/categories/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, category_data: CategoryCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    category_service = CategoryService(db)
    current_user = get_current_user(db, token)
    return category_service.update_category(category_id, category_data, current_user)

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    category_service = CategoryService(db)
    current_user = get_current_user(db, token)
    return category_service.delete_category(category_id, current_user)
