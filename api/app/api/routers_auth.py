# -*- coding: utf-8 -*-
"""
Created on 2025/9/28 21:37

@author: Aidan
@project: GoalBet
@filename: routers_auth
@description: 
- Python 
"""
from typing import Dict

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import EmailStr
from sqlalchemy.orm import Session

from api.app.core.security import hash_password, verify_password, create_access_token, decode_token
from api.app.core.settings import settings
from api.app.models.db_models import User
from api.app.models.user import UserPublic, UserCreate, Token, UserLogin

from api.app.core.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=UserPublic)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    print("Using DB inside /auth/register:", db.bind.url)
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # update the database
    user = User(
        email=str(payload.email),
        hashed_password=hash_password(payload.password),
        balance=settings.initial_balance
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserPublic(id=user.id, email=payload.email)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": payload.email})
    return Token(access_token=token)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        if not payload or "sub" not in payload:
            raise HTTPException(status_code=400, detail="Invalid token")
        email = payload["sub"]
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


@router.get("/me", response_model=UserPublic)
def me(user: User = Depends(get_current_user)):
    return UserPublic(id=user.id, email=user.email)
