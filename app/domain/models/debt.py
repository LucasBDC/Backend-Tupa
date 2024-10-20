from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional

class DebtCreate(BaseModel):
    description: str
    principal_amount: float
    interest_rate: Optional[float] = None
    due_date: date
    total_payments: int

class DebtRead(BaseModel):
    id: int
    description: str
    principal_amount: float
    interest_rate: Optional[float]
    remaining_balance: float
    due_date: date
    payments_made: int
    total_payments: int

    model_config = ConfigDict(from_attributes=True)
