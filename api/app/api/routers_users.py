# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 20:02

@author: Aidan
@project: GoalBet
@filename: routers_users
"""
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from api.app.api.routers_auth import get_current_user
from api.app.core.db import get_db
from api.app.core.security import verify_frontend_key
from api.app.models.bet import BetPublic
from api.app.models.db_models import User
from api.app.service import bet_service

router = APIRouter(prefix="/users", tags=["users"])

limiter = Limiter(key_func=get_remote_address)


class LeaderboardEntry(BaseModel):
    rank: int
    email: str
    balance: int


@router.get("/bets", response_model=list[BetPublic], dependencies=[Depends(verify_frontend_key)])
@limiter.limit("100/minute")
def list_my_bets(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return [BetPublic.model_validate(b) for b in bet_service.get_user_bets(db, user.id)]


@router.get("/leaderboard", response_model=list[LeaderboardEntry], dependencies=[Depends(verify_frontend_key)])
@limiter.limit("60/minute")
def leaderboard(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.balance.desc()).limit(50).all()
    return [LeaderboardEntry(rank=i + 1, email=u.email, balance=u.balance) for i, u in enumerate(users)]
