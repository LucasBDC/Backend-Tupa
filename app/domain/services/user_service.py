import os
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from sqlalchemy.orm import Session
from app.domain.services.auth_service import is_token_blacklisted
from app.infrastructure.database.db import get_db
from app.infrastructure.database.models.user import User
from app.domain.models.user import UserCreate, UserRead
from app.core.security import hash_password
from fastapi import Depends, HTTPException, status

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(self, db: Session, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if is_token_blacklisted(token):
            raise credentials_exception
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise credentials_exception
        return user


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

        return UserRead(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email,
            monthly_budget=new_user.monthly_budget
        )

    def get_user(self, current_user: User) -> UserRead:
        return UserRead(
            id=current_user.id,
            name=current_user.name,
            email=current_user.email,
            monthly_budget=current_user.monthly_budget
        )

    def update_user(self, user_data: UserCreate, current_user: User) -> UserRead:
        user = self.db.query(User).filter(User.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.name = user_data.name
        user.email = user_data.email
        user.monthly_budget = user_data.monthly_budget

        if user_data.password:
            user.password_hash = hash_password(user_data.password)

        self.db.commit()
        self.db.refresh(user)

        return UserRead(
            id=user.id,
            name=user.name,
            email=user.email,
            monthly_budget=user.monthly_budget
        )

    def delete_user(self, current_user: User):
        user = self.db.query(User).filter(User.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        self.db.delete(user)
        self.db.commit()

        return {"detail": "User deleted successfully"}

    def deactivate_user(self, current_user: User):
        user = self.db.query(User).filter(User.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.is_active = False
        self.db.commit()
        self.db.refresh(user)

        return {"detail": "User deactivated successfully"}

    def activate_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.is_active = True
        self.db.commit()
        self.db.refresh(user)

        return {"detail": "User activated successfully"}
