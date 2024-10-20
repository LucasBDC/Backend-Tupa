from sqlalchemy import Column, Integer, String, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from app.infrastructure.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    monthly_budget = Column(DECIMAL(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)

    categories = relationship("Category", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")
    installments = relationship("Installment", back_populates="user")
    debt = relationship("Debt", back_populates="user")
