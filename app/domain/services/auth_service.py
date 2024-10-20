from sqlalchemy.orm import Session
from app.infrastructure.database.models.user import User
from app.core.security import verify_password
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, email: str, password: str):
        user = self.db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is deactivated")
        
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        
        return user
