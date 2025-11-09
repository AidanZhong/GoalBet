# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 20:02

@author: Aidan
@project: GoalBet
@filename: routers_users
"""
from fastapi import APIRouter, Depends, Request
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


@router.get("/bets", response_model=list[BetPublic], dependencies=[Depends(verify_frontend_key)])
@limiter.limit("100/minute")
def list_my_bets(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return [BetPublic.model_validate(b) for b in bet_service.get_user_bets(db, user.id)]
