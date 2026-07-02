from config import SECURITY_KEY, ALGORITHM, TOKEN_TTL, oauth2_scheme
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from typing import Optional
from database import SessionLocal, UserModel
import jwt

def validate_user(username: str, password: str) -> Optional[str]:
    db = SessionLocal()
    user = db.query(UserModel).filter(UserModel.username == username).first()
    db.close()
    if user and user.password == password:
        return username
    return None

def get_user_profile(username: str):
    db = SessionLocal()
    user = db.query(UserModel).filter(UserModel.username == username).first()
    db.close()
    if not user:
        return None
    return {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "age": user.age,
    }

def register_user(username: str, password: str, full_name: str = None, email: str = None, phone: str = None, age: int = None) -> bool:
    db = SessionLocal()
    exists = db.query(UserModel).filter(UserModel.username == username).first()
    if exists:
        db.close()
        return False
    db.add(UserModel(
        username=username,
        password=password,
        full_name=full_name,
        email=email,
        phone=phone,
        age=age
    ))
    db.commit()
    db.close()
    return True

def create_access_token(username: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TTL)
    payload = {"username": username, "exp": expires}
    return jwt.encode(payload, SECURITY_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("username")
        if not username:
            raise credentials_exc
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exc