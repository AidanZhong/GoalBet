# -*- coding: utf-8 -*-
"""
Created on 12/11/2025 23:26

@author: Aidan
@project: GoalBet
@filename: tokens_helper
@description: used for email verification
"""
import base64
import datetime
import hashlib
import os
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.app.core.security import hash_password
from api.app.models.db_models import User, UserToken
from api.app.service.email import send_email


def _raw_token(bytes_len: int = 32) -> str:
    return base64.urlsafe_b64decode(os.urandom(bytes_len)).rstrip(b'=').decode()


def _digest(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def issue_token(db: Session, user_id: int, kind: str, ttl_seconds: int) -> str:
    db.query(UserToken).filter(
        UserToken.user_id == user_id, UserToken.kind == kind, UserToken.consumed_at.is_(None)
    ).update(
        {"consumed_at": datetime.datetime.now(datetime.timezone.utc)},
    )  # update consumed_at to now to avoid multiple valid tokens

    raw = _raw_token()
    digest = _digest(raw)
    expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=ttl_seconds)
    token = UserToken(user_id=user_id, token=digest, kind=kind, expires_at=expires)
    db.add(token)
    db.commit()
    return raw


def consume_token(db: Session, raw: str, kind: str) -> Optional[User]:
    digest = _digest(raw)
    token = (
        db.query(UserToken)
        .filter(
            UserToken.token == digest,
            UserToken.kind == kind,
            UserToken.consumed_at.is_(None),
            UserToken.expires_at > datetime.datetime.now(datetime.timezone.utc),
        )
        .first()
    )
    if not token:
        return None

    token.consumed_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()

    user = db.query(UserToken.user_id).filter(UserToken.id == token.id).first()

    return user


def send_verification_email(user: User, raw_token: str):
    verify_url = f"https://www.goalbet.dev/verify?token={raw_token}"
    send_email(
        to=user.email,
        subject="Verify your email for GoalBet",
        body=f"Please verify your email by clicking the following link: {verify_url}. It will expire in 24 hours.",
    )


def send_reset_password_email(user: User, raw_token: str):
    reset_url = f"https://www.goalbet.dev/reset-password?token={raw_token}"
    send_email(
        to=user.email,
        subject="Reset your password for GoalBet",
        body=f"Please reset your password by clicking the following link: {reset_url}. It will expire in 1 hour.",
    )


def resend_verification_email(db, email):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"ok": True}  # if there is no user, we don't need to send an email, silently return ok
    raw_token = issue_token(db, user.id, "verify", ttl_seconds=60 * 60 * 24)
    send_verification_email(user, raw_token)
    return {"ok": True}


def forgot_password(db, email):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"ok": True}  # same as above, silently return ok
    raw_token = issue_token(db, user.id, "reset", ttl_seconds=60 * 60)  # 1 hour
    send_reset_password_email(user, raw_token)
    return {"ok": True}


def reset_password(db, token, password):
    user = consume_token(db, token, "reset")
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user.hashed_password = hash_password(password)
    db.commit()
    return {"ok": True}
