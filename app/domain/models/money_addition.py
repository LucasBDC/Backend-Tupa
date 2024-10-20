from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class MoneyAdditionCreate(BaseModel):
    amount: float
    description: Optional[str] = None

class MoneyAdditionRead(BaseModel):
    id: int
    amount: float
    description: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
