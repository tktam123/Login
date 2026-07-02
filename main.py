from fastapi.middleware.cors import CORSMiddleware
from auth import create_access_token, validate_user, register_user, get_current_user, get_user_profile
from items import router as items_router 
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import uvicorn
import jwt
from models import Token,UserSignup
from database import init_db

app = FastAPI(title="CRUD API with JWT Auth")
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)


@app.get("/me", tags=["Auth"])
async def me(current_user: str = Depends(get_current_user)):
    profile = get_user_profile(current_user)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile


@app.post("/signup", response_model=Token, tags=["Auth"])
async def signup(body: UserSignup):
    success = register_user(
        username=body.username,
        password=body.password,
        full_name=body.full_name,
        email=body.email,
        phone=body.phone,
        age=body.age
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    return Token(access_token=create_access_token(body.username), token_type="bearer")


# ── Auth route ────────────────────────────────────────────────────────────────
@app.post("/login", response_model=Token, tags=["Auth"])
async def login(form: OAuth2PasswordRequestForm = Depends()):
    username = validate_user(form.username, form.password)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(username), token_type="bearer")

