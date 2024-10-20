from pydantic import BaseModel

class InstallmentCreate(BaseModel):
    total_amount: float
    installment_amount: float
    total_installments: int
    description: str
    category_id: int = None

class InstallmentRead(BaseModel):
    id: int
    total_amount: float
    installment_amount: float
    total_installments: int
    current_installment: int
    description: str

    class Config:
        orm_mode = True
