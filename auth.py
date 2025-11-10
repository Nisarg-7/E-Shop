from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from pydantic import BaseModel
from fastapi import Depends, HTTPException, APIRouter, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
import database_models
from database import session
from database import get_db
from database_models import User
from sqlalchemy import Boolean


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = '/login/')


SECRET_KEY = '16a45ed832ffccbd35cfd9ca4c85e006'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes =['bcrypt'], deprecated = 'auto')

credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers = {"WWW-Authenticate": "Bearer"})


def get_password_hash(plain_password: str) -> str:
    return bcrypt_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, is_admin: bool = False):
    to_encode = data.copy()
    to_encode.update({"is_admin": is_admin})
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
    
def verify_admin(user: User):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
