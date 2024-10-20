from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.db import Base
from datetime import date

class Debt(Base):
    __tablename__ = "debts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    principal_amount = Column(Float, nullable=False)  # Valor original da dívida
    interest_rate = Column(Float, nullable=True)  # Taxa de juros
    remaining_balance = Column(Float, nullable=False)  # Saldo restante
    due_date = Column(Date, nullable=False)  # Data de vencimento
    payments_made = Column(Integer, default=0)  # Número de pagamentos já realizados
    total_payments = Column(Integer, nullable=False)  # Número total de pagamentos

    user = relationship("User", back_populates="debts")
