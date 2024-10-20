from pydantic import BaseModel

class PurchaseCreate(BaseModel):
    category_id: int
    description: str
    amount: float

class PurchaseRead(BaseModel):
    id: int
    description: str
    amount: float

    class Config:
        orm_mode = True
