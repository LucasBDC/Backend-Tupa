from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.infrastructure.database.db import Base
from datetime import date
import enum

class FrequencyEnum(str, enum.Enum):
    monthly = "monthly"
    yearly = "yearly"
    weekly = "weekly"
    custom = "custom"  # Para assinaturas com intervalos não padrão

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    frequency = Column(Enum(FrequencyEnum), nullable=False)
    next_payment_date = Column(Date, nullable=False)
    custom_interval = Column(Integer, nullable=True)  # Usado apenas se a frequência for "custom"
    active = Column(Integer, default=True)

    user = relationship("User", back_populates="subscriptions")
