# -*- coding: utf-8 -*-
"""
Created on 2025/10/2 21:57

@author: Aidan
@project: GoalBet
@filename: routers_bets
@description: 
- Python 
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.app.api.routers_auth import get_current_user
from api.app.api.routers_stream import broadcast
from api.app.core.db import get_db
from api.app.models.bet import BetPublic, BetCreate, BetSide, BetStatus
from api.app.models.db_models import Goal, User, Bet
from api.app.models.enums import GoalStatus

router = APIRouter(prefix="/markets", tags=["bets"])


@router.post("/{goal_id}/bets", response_model=BetPublic)
def place_bet(goal_id: int, payload: BetCreate, user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    if goal.status != GoalStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Market is closed")

    if user.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # update the pool
    total_pool = db.query(func.coalesce(func.sum(Bet.amount), 0)).filter(Bet.goal_id == goal_id).scalar()
    side_pool = db.query(func.coalesce(func.sum(Bet.amount), 0)).filter(Bet.goal_id == goal_id,
                                                                        Bet.side == payload.side).scalar()
    total_pool += payload.amount
    side_pool += payload.amount

    # deduct from wallet
    user.balance -= payload.amount

    # calc odds, using parimutuel method
    odds = round(total_pool / side_pool, 2) if side_pool > 0 else 1

    bet = Bet(
        goal_id=goal_id,
        user_id=user.id,
        side=payload.side,
        amount=payload.amount,
        odds_snapshot=odds,
        status=BetStatus.PENDING
    )
    db.add(bet)
    db.commit()
    db.refresh(bet)
    broadcast("bet.placed", {
        "goal_id": goal_id,
        "user_email": user.email,
        "side": payload.side.value,
        "amount": payload.amount,
        "odds_snapshot": odds
    })
    betPublic = BetPublic.model_validate(bet)
    return betPublic


@router.get("/{goal_id}/bets", response_model=List[BetPublic])
def list_bets(goal_id: int, db: Session = Depends(get_db)):
    return [BetPublic.model_validate(b) for b in
            db.query(Bet).filter(Bet.goal_id == goal_id).all()]
