from typing import Optional
from sqlalchemy.orm import Session
from app.infrastructure.database.models.subscription import Subscription
from app.infrastructure.database.models.category import Category
from app.infrastructure.database.models.user import User
from app.domain.models.subscription import SubscriptionCreate, SubscriptionRead
from fastapi import HTTPException, status
from datetime import timedelta, date

class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db

    def create_subscription(self, current_user: User, subscription_data: SubscriptionCreate) -> SubscriptionRead:
        next_payment_date = self.calculate_next_payment_date(subscription_data.frequency, subscription_data.next_payment_date, subscription_data.custom_interval)

        new_subscription = Subscription(
            user_id=current_user.id,
            service_name=subscription_data.service_name,
            description=subscription_data.description,
            amount=subscription_data.amount,
            frequency=subscription_data.frequency,
            next_payment_date=next_payment_date,
            custom_interval=subscription_data.custom_interval
        )

        self.db.add(new_subscription)
        self.db.commit()
        self.db.refresh(new_subscription)

        return SubscriptionRead.model_validate(new_subscription)

    def calculate_next_payment_date(self, frequency: str, current_date: date, custom_interval: Optional[int]) -> date:
        if frequency == "monthly":
            return current_date + timedelta(days=30)
        elif frequency == "yearly":
            return current_date + timedelta(days=365)
        elif frequency == "weekly":
            return current_date + timedelta(weeks=1)
        elif frequency == "custom" and custom_interval:
            return current_date + timedelta(days=custom_interval)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid frequency or custom interval")

    def process_due_subscriptions(self):
        today = date.today()
        subscriptions = self.db.query(Subscription).filter(Subscription.next_payment_date <= today, Subscription.active == 1).all()

        for subscription in subscriptions:
            user = self.db.query(User).filter(User.id == subscription.user_id).first()
            if user.monthly_budget < subscription.amount:
                # Se o usuário não tiver saldo suficiente, você pode optar por enviar uma notificação
                # e continuar para a próxima assinatura sem deduzir o valor.
                continue

            user.monthly_budget -= subscription.amount

            subscription.next_payment_date = self.calculate_next_payment_date(
                subscription.frequency, subscription.next_payment_date, subscription.custom_interval
            )

            self.db.commit()
            self.db.refresh(user)
            self.db.refresh(subscription)

        return {"detail": "Processed due subscriptions"}
