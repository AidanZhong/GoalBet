# -*- coding: utf-8 -*-
"""
Created on 2025/9/28 21:53

@author: Aidan
@project: GoalBet
@filename: routers_wallet
"""
from fastapi import APIRouter, Depends

from api.app.api.routers_auth import get_current_user
from api.app.models.db_models import User

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("")
def get_wallet(user: User = Depends(get_current_user)):
    return {"balance": user.balance}
