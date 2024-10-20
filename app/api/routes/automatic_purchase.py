from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.db import get_db
from app.domain.models.automatic_purchase import AutomaticPurchaseCreate, AutomaticPurchaseRead
from app.domain.services.automatic_purchase_service import AutomaticPurchaseService
from app.domain.services.user_service import get_current_user
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/automatic_purchases", response_model=AutomaticPurchaseRead)
def create_automatic_purchase(purchase_data: AutomaticPurchaseCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    purchase_service = AutomaticPurchaseService(db)
    current_user = get_current_user(db, token)
    return purchase_service.create_automatic_purchase(current_user, purchase_data)

@router.get("/automatic_purchases", response_model=list[AutomaticPurchaseRead])
def get_user_automatic_purchases(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    purchase_service = AutomaticPurchaseService(db)
    current_user = get_current_user(db, token)
    return purchase_service.get_user_automatic_purchases(current_user)
