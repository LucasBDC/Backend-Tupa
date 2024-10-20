from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.db import get_db
from app.domain.models.money_addition import MoneyAdditionCreate, MoneyAdditionRead
from app.domain.services.money_addition_service import MoneyAdditionService
from app.domain.services.user_service import get_current_user
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/add_money", response_model=MoneyAdditionRead)
def add_money(addition_data: MoneyAdditionCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    money_addition_service = MoneyAdditionService(db)
    current_user = get_current_user(db, token)
    return money_addition_service.add_money(current_user, addition_data)

@router.get("/money_additions", response_model=list[MoneyAdditionRead])
def get_user_money_additions(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    money_addition_service = MoneyAdditionService(db)
    current_user = get_current_user(db, token)
    return money_addition_service.get_user_money_additions(current_user)
