# -*- coding: utf-8 -*-
"""
Created on 2025/9/28 21:37

@author: Aidan
@project: GoalBet
@filename: routers_auth
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app.core.db import get_db
from api.app.core.security import verify_frontend_key
from api.app.models.db_models import User
from api.app.models.user import Token, UserCreate, UserLogin, UserPublic
from api.app.service.user_service import create_user, get_current_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, dependencies=[Depends(verify_frontend_key)])
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, str(payload.email), payload.password)
    return UserPublic(id=user.id, email=payload.email)


@router.post("/login", response_model=Token, dependencies=[Depends(verify_frontend_key)])
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, str(payload.email), payload.password)


@router.get("/me", response_model=UserPublic, dependencies=[Depends(verify_frontend_key)])
def me(user: User = Depends(get_current_user)):
    return UserPublic(id=user.id, email=user.email)
