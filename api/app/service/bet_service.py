# -*- coding: utf-8 -*-
"""
Created on 2025/10/14 20:29

@author: Aidan
@project: GoalBet
@filename: bet_service
"""

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.app.core.events import broadcast
from api.app.models.bet import BetCreate, BetStatus
from api.app.models.db_models import Bet, Goal, User
from api.app.models.enums import GoalStatus


def place_bet(db: Session, goal_id: int, payload: BetCreate, user: User, background_tasks):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    if goal.status != GoalStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Market is closed")

    if user.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # update the pool
    total_pool = (
        db.query(func.coalesce(func.sum(Bet.amount), 0)).filter(Bet.goal_id == goal_id).scalar()
    )
    side_pool = (
        db.query(func.coalesce(func.sum(Bet.amount), 0))
        .filter(Bet.goal_id == goal_id, Bet.side == payload.side)
        .scalar()
    )
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
        status=BetStatus.PENDING,
    )
    db.add(bet)
    db.commit()
    db.refresh(bet)
    background_tasks.add_task(
        broadcast,
        "bet.placed",
        {
            "goal_id": goal_id,
            "user_email": user.email,
            "side": payload.side.value,
            "amount": payload.amount,
            "odds_snapshot": odds,
        },
    )
    return bet


def get_bets(db: Session, goal_id: int):
    return db.query(Bet).filter(Bet.goal_id == goal_id).all()


def get_user_bets(db: Session, user_id: int):
    return db.query(Bet).filter(Bet.user_id == user_id).all()
