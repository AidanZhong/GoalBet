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

from api.app.core.security import hash_password, verify_password, create_access_token, decode_token
from api.app.core.settings import settings
from api.app.models.user import UserPublic, UserCreate, Token, UserLogin
from api.app.core import data_store

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=UserPublic)
def register(payload: UserCreate):
    if payload.email in data_store._db:
        raise HTTPException(status_code=400, detail="Email already registered")

    # update the database
    data_store._user_id = data_store._user_id + 1
    data_store._db[payload.email] = {
        "id": data_store._user_id,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "balance": settings.initial_balance
    }

    return {"id": data_store._user_id, "email": payload.email}


@router.post("/login", response_model=Token)
def login(payload: UserLogin):
    user = data_store._db.get(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({"sub": payload.email})
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=400, detail="Invalid token")
    email = payload["sub"]
    user = data_store._db.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/me", response_model=UserPublic)
def me(user: dict = Depends(get_current_user)):
    return {"id": user["id"], "email": user["email"]}
