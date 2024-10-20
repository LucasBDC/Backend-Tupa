from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database.models.user import User
from app.core.security import create_access_token, verify_password
from datetime import timedelta

BLACKLIST = set()

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return False
    return user

def login(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

def logout(token: str):
    BLACKLIST.add(token)

def is_token_blacklisted(token: str) -> bool:
    return token in BLACKLIST
