# -*- coding: utf-8 -*-
"""
Created on 2025/10/14 19:30

@author: Aidan
@project: GoalBet
@filename: user_service
"""
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from api.app.core.db import get_db
from api.app.core.security import create_access_token, decode_token, hash_password, verify_password
from api.app.core.settings import settings
from api.app.models.db_models import User
from api.app.models.user import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_user(
    db: Session, email: str, password: str, initial_balance: int = settings.initial_balance
) -> User:
    exists = db.query(User).filter(User.email == email).first()
    if exists:
        raise ValueError("User already exists")
    hashed_password = hash_password(password)
    user = User(email=str(email), hashed_password=hashed_password, balance=initial_balance)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


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


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": email})
    return Token(access_token=token)
