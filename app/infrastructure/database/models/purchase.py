from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.infrastructure.database.db import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    purchased_at = Column(TIMESTAMP, server_default=func.now())

    # Relacionamentos
    user = relationship("User", back_populates="purchases")
    category = relationship("Category", back_populates="purchases") 
