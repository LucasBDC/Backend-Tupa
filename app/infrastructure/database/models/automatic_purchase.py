from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from app.infrastructure.database.db import Base
from datetime import datetime
import enum

class FrequencyEnum(str, enum.Enum):
    daily = "daily"
    every_other_day = "every_other_day"
    weekly = "weekly"
    every_other_week = "every_other_week"
    monthly = "monthly"
    every_other_month = "every_other_month"
    every_three_months = "every_three_months"
    every_six_months = "every_six_months"
    yearly = "yearly"

class AutomaticPurchase(Base):
    __tablename__ = "automatic_purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    frequency = Column(Enum(FrequencyEnum), nullable=False)
    start_date = Column(Date, nullable=False, default=datetime.utcnow)
    next_run = Column(Date, nullable=False)
    active = Column(Integer, default=True)

    user = relationship("User", back_populates="automatic_purchases")
    category = relationship("Category", back_populates="automatic_purchases")
