# -*- coding: utf-8 -*-
"""
Created on 2025/9/28 21:26

@author: Aidan
@project: GoalBet
@filename: security
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Header, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

from api.app.core.settings import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc)
    if expires_delta:
        expire += expires_delta
    else:
        expire += timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.encrypt_algorithm)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.encrypt_algorithm])
    except JWTError:
        return None


def verify_frontend_key(x_api_key: str = Header(None)):
    # skip the check in test environment
    if settings.env in ("test", "development", "local", "debug"):
        return

    if x_api_key != settings.frontend_api_key:
        raise HTTPException(status_code=403, detail="Forbidden")
