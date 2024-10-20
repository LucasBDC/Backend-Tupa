from sqlalchemy.orm import Session
from app.infrastructure.database.models.automatic_purchase import AutomaticPurchase
from app.infrastructure.database.models.category import Category
from app.domain.models.automatic_purchase import AutomaticPurchaseCreate, AutomaticPurchaseRead
from fastapi import HTTPException, status
from datetime import date, timedelta
from app.infrastructure.database.models.user import User

class AutomaticPurchaseService:
    def __init__(self, db: Session):
        self.db = db

    def create_automatic_purchase(self, current_user: User, purchase_data: AutomaticPurchaseCreate) -> AutomaticPurchaseRead:
        category = self.db.query(Category).filter(Category.id == purchase_data.category_id, Category.user_id == current_user.id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found or doesn't belong to user")
        
        next_run = self.calculate_next_run(purchase_data.frequency, purchase_data.start_date)

        new_automatic_purchase = AutomaticPurchase(
            user_id=current_user.id,
            category_id=purchase_data.category_id,
            description=purchase_data.description,
            amount=purchase_data.amount,
            frequency=purchase_data.frequency,
            start_date=purchase_data.start_date,
            next_run=next_run
        )

        self.db.add(new_automatic_purchase)
        self.db.commit()
        self.db.refresh(new_automatic_purchase)

        return AutomaticPurchaseRead.model_validate(new_automatic_purchase)

    def calculate_next_run(self, frequency: str, start_date: date) -> date:
        if frequency == "daily":
            return start_date + timedelta(days=1)
        elif frequency == "every_other_day":
            return start_date + timedelta(days=2)
        elif frequency == "weekly":
            return start_date + timedelta(weeks=1)
        elif frequency == "every_other_week":
            return start_date + timedelta(weeks=2)
        elif frequency == "monthly":
            return start_date + timedelta(days=30)
        elif frequency == "every_other_month":
            return start_date + timedelta(days=60)
        elif frequency == "every_three_months":
            return start_date + timedelta(days=90)
        elif frequency == "every_six_months":
            return start_date + timedelta(days=180)
        elif frequency == "yearly":
            return start_date + timedelta(days=365)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid frequency")

    def process_automatic_purchases(self):
        today = date.today()
        automatic_purchases = self.db.query(AutomaticPurchase).filter(AutomaticPurchase.next_run <= today, AutomaticPurchase.active == 1).all()

        for purchase in automatic_purchases:
            category = self.db.query(Category).filter(Category.id == purchase.category_id, Category.user_id == purchase.user_id).first()
            if not category:
                continue

            if category.remaining_amount >= purchase.amount:
                category.remaining_amount -= purchase.amount
                self.db.commit()

                purchase.next_run = self.calculate_next_run(purchase.frequency, purchase.next_run)
                self.db.commit()
            else:
                continue
