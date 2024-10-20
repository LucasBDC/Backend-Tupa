from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date
from enum import Enum

class FrequencyEnum(str, Enum):
    daily = "daily"
    every_other_day = "every_other_day"
    weekly = "weekly"
    every_other_week = "every_other_week"
    monthly = "monthly"
    every_other_month = "every_other_month"
    every_three_months = "every_three_months"
    every_six_months = "every_six_months"
    yearly = "yearly"

class AutomaticPurchaseCreate(BaseModel):
    category_id: int
    description: str
    amount: float
    frequency: FrequencyEnum
    start_date: Optional[date] = Field(default_factory=date.today)

class AutomaticPurchaseRead(BaseModel):
    id: int
    user_id: int
    category_id: int
    description: str
    amount: float
    frequency: FrequencyEnum
    start_date: date
    next_run: date
    active: bool

    model_config = ConfigDict(from_attributes=True)
