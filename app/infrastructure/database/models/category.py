from sqlalchemy import Column, Integer, String, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.db import Base
import enum

class CategoryPeriod(str, enum.Enum):
    weekly = "weekly"
    monthly = "monthly"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    planned_amount = Column(DECIMAL(10, 2), nullable=False)
    remaining_amount = Column(DECIMAL(10, 2), nullable=False)
    period = Column(Enum(CategoryPeriod), nullable=False)

    user = relationship("User", back_populates="categories")
    purchases = relationship("Purchase", back_populates="category") 
    installments = relationship("Installment", back_populates="category") 
