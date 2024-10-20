from sqlalchemy.orm import Session
from app.infrastructure.database.models.debt import Debt
from app.domain.models.debt import DebtCreate, DebtRead
from app.infrastructure.database.models.user import User
from fastapi import HTTPException, status
from datetime import date

class DebtService:
    def __init__(self, db: Session):
        self.db = db

    def create_debt(self, current_user: User, debt_data: DebtCreate) -> DebtRead:
        new_debt = Debt(
            user_id=current_user.id,
            description=debt_data.description,
            principal_amount=debt_data.principal_amount,
            remaining_balance=debt_data.principal_amount,
            interest_rate=debt_data.interest_rate,
            due_date=debt_data.due_date,
            total_payments=debt_data.total_payments,
        )

        self.db.add(new_debt)
        self.db.commit()
        self.db.refresh(new_debt)

        return DebtRead.model_validate(new_debt)

    def make_payment(self, debt_id: int, current_user: User, payment_amount: float) -> DebtRead:
        debt = self.db.query(Debt).filter(Debt.id == debt_id, Debt.user_id == current_user.id).first()
        if not debt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debt not found")

        if debt.remaining_balance < payment_amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment exceeds remaining balance")

        debt.remaining_balance -= payment_amount
        debt.payments_made += 1

        self.db.commit()
        self.db.refresh(debt)

        return DebtRead.model_validate(debt)

    def get_user_debts(self, current_user: User) -> list[DebtRead]:
        debts = self.db.query(Debt).filter(Debt.user_id == current_user.id).all()
        return [DebtRead.model_validate(debt) for debt in debts]
