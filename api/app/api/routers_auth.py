# -*- coding: utf-8 -*-
"""
Created on 2025/9/28 21:37

@author: Aidan
@project: GoalBet
@filename: routers_auth
"""
import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from api.app.core.db import get_db
from api.app.core.security import verify_frontend_key
from api.app.models.db_models import User
from api.app.models.user import ForgotIn, ResetIn, Token, UserCreate, UserLogin, UserPublic
from api.app.service import tokens_helper
from api.app.service.tokens_helper import consume_token, issue_token, resend_verification_email, send_verification_email
from api.app.service.user_service import create_user, get_current_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])

limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserPublic, dependencies=[Depends(verify_frontend_key)])
@limiter.limit("10/minute")
def register(request: Request, payload: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, str(payload.email), payload.password)
    raw = issue_token(db, user_id=user.id, kind="verify", ttl_seconds=60 * 60 * 24)
    send_verification_email(user, raw)
    return UserPublic(id=user.id, email=payload.email)


@router.post("/login", response_model=Token, dependencies=[Depends(verify_frontend_key)])
@limiter.limit("10/minute")
def login(request: Request, payload: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, str(payload.email), payload.password)


@router.get("/me", response_model=UserPublic, dependencies=[Depends(verify_frontend_key)])
@limiter.limit("100/minute")
def me(request: Request, user: User = Depends(get_current_user)):
    return UserPublic(id=user.id, email=user.email)


@router.get("/verify", dependencies=[Depends(verify_frontend_key)])
@limiter.limit("5/minute")
def verify_email(request: Request, token: str, db: Session = Depends(get_db)):
    user = consume_token(db, token, kind="verify")
    if not user:
        raise HTTPException(status_code=400, detail="user not exists or invalid/expired token")
    user.email_verified_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    return {"Message": "Email verified"}


@router.post("/verify/resend", dependencies=[Depends(verify_frontend_key)])
@limiter.limit("5/minute")
def resend_verification(request: Request, email: str, db: Session = Depends(get_db)):
    return resend_verification_email(db, email)


@router.post("/forgot_password", dependencies=[Depends(verify_frontend_key)])
@limiter.limit("5/minute")
def forgot_password(request: Request, payload: ForgotIn, db: Session = Depends(get_db)):
    return tokens_helper.forgot_password(db, payload.email)


@router.post('/reset', dependencies=[Depends(verify_frontend_key)])
@limiter.limit("5/minute")
def reset(request: Request, payload: ResetIn, db: Session = Depends(get_db)):
    return tokens_helper.reset_password(db, payload.token, payload.password)
