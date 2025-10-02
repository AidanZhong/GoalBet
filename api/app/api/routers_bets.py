# -*- coding: utf-8 -*-
"""
Created on 2025/10/2 21:57

@author: Aidan
@project: GoalBet
@filename: routers_bets
@description: 
- Python 
"""
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException

from api.app.api.routers_auth import get_current_user
from api.app.api.routers_stream import broadcast
from api.app.models.bet import BetPublic, BetCreate, BetSide
from api.app.api.routers_goals import _goals

router = APIRouter(prefix="/markets", tags=["bets"])

_bets: Dict[int, List[dict]] = {}
_bet_id = 0
_pools: Dict[int, Dict[str, int]] = {}


@router.post("/{goal_id}/bets", response_model=BetPublic)
def place_bet(goal_id: int, payload: BetCreate, user: dict = Depends(get_current_user)):
    global _bet_id

    goal = _goals.get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    if user['balance'] < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # init the pool
    if goal_id not in _pools:
        _pools[goal_id] = {BetSide.SUCCESS: 0, BetSide.FAIL: 0}
        _bets[goal_id] = []

    # update the pool
    _pools[goal_id][payload.side.value] += payload.amount

    # deduct from wallet
    user['balance'] -= payload.amount

    # calc odds, using parimutuel method
    total_pool = sum(_pools[goal_id].values())
    side_pool = _pools[goal_id][payload.side.value]
    odds = round(total_pool / side_pool, 2) if side_pool > 0 else 1

    _bet_id += 1
    bet = {
        "id": _bet_id,
        "goal_id": goal_id,
        "user_email": user["email"],
        "side": payload.side.value,
        "amount": payload.amount,
        "odds_snapshot": odds
    }

    _bets[goal_id].append(bet)
    broadcast("bet.placed", bet)
    return bet

@router.get("/{goal_id}/bets", response_model=List[BetPublic])
def list_bets(goal_id: int):
    return _bets.get(goal_id, [])

