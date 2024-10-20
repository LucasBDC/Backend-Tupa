from sqlalchemy.orm import Session
from app.infrastructure.database.models.user import User
from app.domain.models.user import UserCreate, UserRead
from app.core.security import hash_password
from fastapi import HTTPException, status

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> UserRead:
        existing_user = self.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        hashed_password = hash_password(user_data.password)

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
            monthly_budget=user_data.monthly_budget
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def get_user_by_id(self, user_id: int) -> UserRead:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def update_user(self, user_id: int, user_data: UserCreate) -> UserRead:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.name = user_data.name
        user.email = user_data.email
        user.monthly_budget = user_data.monthly_budget

        if user_data.password:
            user.password_hash = hash_password(user_data.password)

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        self.db.delete(user)
        self.db.commit()
        return {"detail": "User deleted successfully"}
