from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.db import get_db
from app.domain.models.purchase import PurchaseCreate, PurchaseRead
from app.domain.services.purchase_service import PurchaseService
from app.domain.services.user_service import get_current_user
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/purchases", response_model=PurchaseRead)
def create_purchase(purchase_data: PurchaseCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    purchase_service = PurchaseService(db)
    current_user = get_current_user(db, token)
    return purchase_service.create_purchase(current_user, purchase_data)

@router.get("/purchases", response_model=list[PurchaseRead])
def get_user_purchases(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    purchase_service = PurchaseService(db)
    current_user = get_current_user(db, token)
    return purchase_service.get_user_purchases(current_user)

@router.get("/purchases/{purchase_id}", response_model=PurchaseRead)
def get_purchase(purchase_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    purchase_service = PurchaseService(db)
    current_user = get_current_user(db, token)
    return purchase_service.get_purchase_by_id(purchase_id, current_user)

@router.put("/purchases/{purchase_id}", response_model=PurchaseRead)
def update_purchase(purchase_id: int, purchase_data: PurchaseCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    purchase_service = PurchaseService(db)
    current_user = get_current_user(db, token)
    return purchase_service.update_purchase(purchase_id, purchase_data, current_user)

@router.delete("/purchases/{purchase_id}")
def delete_purchase(purchase_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    purchase_service = PurchaseService(db)
    current_user = get_current_user(db, token)
    return purchase_service.delete_purchase(purchase_id, current_user)
