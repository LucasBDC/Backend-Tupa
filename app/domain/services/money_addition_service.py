from sqlalchemy.orm import Session
from app.infrastructure.database.models.money_addition import MoneyAddition
from app.infrastructure.database.models.user import User
from app.domain.models.money_addition import MoneyAdditionCreate, MoneyAdditionRead
from fastapi import HTTPException, status

class MoneyAdditionService:
    def __init__(self, db: Session):
        self.db = db

    def add_money(self, current_user: User, addition_data: MoneyAdditionCreate) -> MoneyAdditionRead:
        # Atualiza o saldo do usuário
        current_user.monthly_budget += addition_data.amount

        # Cria uma nova transação de adição de dinheiro
        new_addition = MoneyAddition(
            user_id=current_user.id,
            amount=addition_data.amount,
            description=addition_data.description
        )

        self.db.add(new_addition)
        self.db.commit()
        self.db.refresh(new_addition)
        self.db.refresh(current_user)

        return MoneyAdditionRead.model_validate(new_addition)

    def get_user_money_additions(self, current_user: User) -> list[MoneyAdditionRead]:
        additions = self.db.query(MoneyAddition).filter(MoneyAddition.user_id == current_user.id).all()
        return [MoneyAdditionRead.model_validate(addition) for addition in additions]
