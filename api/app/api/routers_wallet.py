# -*- coding: utf-8 -*-
"""
Created on 2025/9/28 21:53

@author: Aidan
@project: GoalBet
@filename: routers_wallet
@description: 
- Python 
"""
from fastapi import APIRouter, Depends

from api.app.api.routers_auth import get_current_user

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("")
def get_wallet(user: dict = Depends(get_current_user)):
    return {"balance": user["balance"]}
