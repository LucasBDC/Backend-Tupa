from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.domain.services.auth_service import login, logout
from app.infrastructure.database.db import get_db
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/auth/login")
def login_route(email: str, password: str, db: Session = Depends(get_db)):
    return login(db, email, password)

@router.post("/auth/logout")
def logoff(token: str = Depends(oauth2_scheme)):
    logout(token)
    return {"detail": "Successfully logged out"}
