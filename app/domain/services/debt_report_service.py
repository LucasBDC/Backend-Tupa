from sqlalchemy.orm import Session
from app.infrastructure.database.models.debt import Debt
from app.domain.models.debt import DebtRead
from app.infrastructure.database.models.user import User

class DebtReportService:
    def __init__(self, db: Session):
        self.db = db

    def generate_debt_summary(self, current_user: User) -> dict:
        debts = self.db.query(Debt).filter(Debt.user_id == current_user.id).all()
        total_debt = sum(debt.remaining_balance for debt in debts)
        total_payments = sum(debt.principal_amount - debt.remaining_balance for debt in debts)

        return {
            "total_debt": total_debt,
            "total_payments_made": total_payments,
            "debts": [DebtRead.model_validate(debt) for debt in debts]
        }
