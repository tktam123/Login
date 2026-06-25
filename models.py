from pydantic import BaseModel
from typing import Optional
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