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
from api.app.service.user_service import create_user, login_user, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, str(payload.email), payload.password)
    return UserPublic(id=user.id, email=payload.email)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, str(payload.email), payload.password)


@router.get("/me", response_model=UserPublic)
def me(user: User = Depends(get_current_user)):
    return UserPublic(id=user.id, email=user.email)
