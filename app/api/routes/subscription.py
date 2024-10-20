from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.db import get_db
from app.domain.models.subscription import SubscriptionCreate, SubscriptionRead
from app.domain.services.subscription_service import SubscriptionService
from app.domain.services.user_service import get_current_user
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/subscriptions", response_model=SubscriptionRead)
def create_subscription(subscription_data: SubscriptionCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    subscription_service = SubscriptionService(db)
    current_user = get_current_user(db, token)
    return subscription_service.create_subscription(current_user, subscription_data)

@router.get("/subscriptions", response_model=list[SubscriptionRead])
def get_user_subscriptions(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    subscription_service = SubscriptionService(db)
    current_user = get_current_user(db, token)
    return subscription_service.get_user_subscriptions(current_user)

@router.patch("/subscriptions/{subscription_id}/deactivate")
def deactivate_subscription(subscription_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    subscription_service = SubscriptionService(db)
    current_user = get_current_user(db, token)
    return subscription_service.deactivate_subscription(subscription_id, current_user)
