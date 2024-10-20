from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.db import get_db
from app.domain.models.installment import InstallmentCreate, InstallmentRead
from app.domain.services.installment_service import InstallmentService
from app.domain.services.user_service import get_current_user
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/installments", response_model=InstallmentRead)
def create_installment(installment_data: InstallmentCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    installment_service = InstallmentService(db)
    current_user = get_current_user(db, token)
    return installment_service.create_installment(current_user, installment_data)

@router.get("/installments", response_model=list[InstallmentRead])
def get_user_installments(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    installment_service = InstallmentService(db)
    current_user = get_current_user(db, token)
    return installment_service.get_user_installments(current_user)

@router.get("/installments/{installment_id}", response_model=InstallmentRead)
def get_installment(installment_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    installment_service = InstallmentService(db)
    current_user = get_current_user(db, token)
    return installment_service.get_installment_by_id(installment_id, current_user)

@router.put("/installments/{installment_id}", response_model=InstallmentRead)
def update_installment(installment_id: int, installment_data: InstallmentCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    installment_service = InstallmentService(db)
    current_user = get_current_user(db, token)
    return installment_service.update_installment(installment_id, installment_data, current_user)

@router.patch("/installments/{installment_id}/pay", response_model=InstallmentRead)
def pay_installment(installment_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    installment_service = InstallmentService(db)
    current_user = get_current_user(db, token)
    return installment_service.pay_installment(installment_id, current_user)

@router.delete("/installments/{installment_id}")
def delete_installment(installment_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    installment_service = InstallmentService(db)
    current_user = get_current_user(db, token)
    return installment_service.delete_installment(installment_id, current_user)
