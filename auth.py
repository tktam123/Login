from config import SECURITY_KEY, ALGORITHM, TOKEN_TTL, oauth2_scheme
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
import jwt
from config import SECURITY_KEY
USERS = {"jack": "111", "admin": "admin123"}
# ── Auth helpers ──────────────────────────────────────────────────────────────
def validate_user(username: str, password: str) -> Optional[str]:
    """Return username if credentials are valid, else None."""
    if USERS.get(username) == password:
        return username
    return None


def create_access_token(username: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TTL)
    payload = {"username": username, "exp": expires}
    return jwt.encode(payload, SECURITY_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Decode the JWT and return the username.
    Raises 401 if the token is missing, expired, or invalid.
    """
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

