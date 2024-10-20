from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from enum import Enum
from typing import Optional

class FrequencyEnum(str, Enum):
    monthly = "monthly"
    yearly = "yearly"
    weekly = "weekly"
    custom = "custom"

class SubscriptionCreate(BaseModel):
    service_name: str
    description: Optional[str] = None
    amount: float
    frequency: FrequencyEnum
    next_payment_date: date
    custom_interval: Optional[int] = None

class SubscriptionRead(BaseModel):
    id: int
    service_name: str
    description: Optional[str]
    amount: float
    frequency: FrequencyEnum
    next_payment_date: date
    custom_interval: Optional[int]
    active: bool

    model_config = ConfigDict(from_attributes=True)
