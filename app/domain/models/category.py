from pydantic import BaseModel
from enum import Enum

class CategoryPeriod(str, Enum):
    weekly = "weekly"
    monthly = "monthly"

class CategoryCreate(BaseModel):
    name: str
    planned_amount: float
    remaining_amount: float
    period: CategoryPeriod

class CategoryRead(BaseModel):
    id: int
    name: str
    planned_amount: float
    remaining_amount: float
    period: CategoryPeriod

    class Config:
        orm_mode = True
