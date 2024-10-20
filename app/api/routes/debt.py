from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.db import get_db
from app.domain.models.debt import DebtCreate, DebtRead
from app.domain.services.debt_service import DebtService
from app.domain.services.user_service import get_current_user
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/debts", response_model=DebtRead)
def create_debt(debt_data: DebtCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    debt_service = DebtService(db)
    current_user = get_current_user(db, token)
    return debt_service.create_debt(current_user, debt_data)

@router.get("/debts", response_model=list[DebtRead])
def get_user_debts(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    debt_service = DebtService(db)
    current_user = get_current_user(db, token)
    return debt_service.get_user_debts(current_user)

@router.post("/debts/{debt_id}/pay", response_model=DebtRead)
def make_payment(debt_id: int, payment_amount: float, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    debt_service = DebtService(db)
    current_user = get_current_user(db, token)
    return debt_service.make_payment(debt_id, current_user, payment_amount)
