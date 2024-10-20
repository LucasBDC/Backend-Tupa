from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    monthly_budget: float

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    monthly_budget: float

    class Config:
        orm_mode = True
