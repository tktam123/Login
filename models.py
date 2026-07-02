from pydantic import BaseModel,field_validator
from typing import Optional
import re
# ── Pydantic models ───────────────────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ItemOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner: str

class UserSignup(BaseModel):
    username:  str
    password:  str
    full_name: Optional[str] = None
    email:     Optional[str] = None
    phone:     Optional[str] = None
    age:       Optional[int] = None

    @field_validator("username")
    def username_valid(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v

    @field_validator("password")
    def password_valid(cls, v):
        if len(v) < 3:
            raise ValueError("Password must be at least 3 characters")
        return v

    @field_validator("phone")
    def phone_valid(cls, v):
        if v is None:
            return v
        cleaned = v.replace(" ", "").replace("-", "")
        if not re.match(r"^\+?[0-9]{7,15}$", cleaned):
            raise ValueError("Phone must be numbers only")
        return v

    @field_validator("age")
    def age_valid(cls, v):
        if v is None:
            return v
        if v < 1 or v > 120:
            raise ValueError("Age must be between 1 and 120")
        return v

    @field_validator("email")
    def email_valid(cls, v):
        if v is None:
            return v
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email address")
        return v
    
class UserOut(BaseModel):
    username:  str
    full_name: Optional[str]
    email:     Optional[str]
    phone:     Optional[str]
    age:       Optional[int]