# -*- coding: utf-8 -*-
"""
Created on 2025/9/28 21:53

@author: Aidan
@project: GoalBet
@filename: routers_wallet
"""
from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.app.api.routers_auth import get_current_user
from api.app.core.security import verify_frontend_key
from api.app.models.db_models import User

router = APIRouter(prefix="/wallet", tags=["wallet"])

limiter = Limiter(key_func=get_remote_address)


@router.get("", dependencies=[Depends(verify_frontend_key)])
@limiter.limit("100/minute")
def get_wallet(request: Request, user: User = Depends(get_current_user)):
    return {"balance": user.balance}
