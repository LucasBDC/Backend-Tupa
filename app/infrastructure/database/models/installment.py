from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.db import Base

class Installment(Base):
    __tablename__ = "installments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    installment_amount = Column(DECIMAL(10, 2), nullable=False)
    total_installments = Column(Integer, nullable=False)
    current_installment = Column(Integer, nullable=False, default=1)
    description = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    purchased_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="installments")
    category = relationship("Category", back_populates="installments")