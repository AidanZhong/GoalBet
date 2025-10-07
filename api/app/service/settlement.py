# -*- coding: utf-8 -*-
"""
Created on 2025/10/3 9:25

@author: Aidan
@project: GoalBet
@filename: settlement
@description: 
- Python 
"""
from fastapi import HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.app.core.db import get_db
from api.app.models.bet import BetStatus
from api.app.models.db_models import Goal, Bet


def resolve_market(goal_id: int, outcome: str, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    bets = db.query(Bet).filter(Bet.goal_id == goal_id).all()
    if not bets:
        # no bets so no settlement
        return []

    total_pool = db.query(func.coalesce(func.sum(Bet.amount), 0)).filter(Bet.goal_id == goal_id).scalar()
    winning_pool = db.query(func.coalesce(func.sum(Bet.amount), 0)).filter(Bet.goal_id == goal_id,
                                                                           Bet.side == outcome).scalar()

    results = []
    for bet in bets:
        if bet.side == outcome:
            # winning side
            odds = total_pool / winning_pool if winning_pool > 0 else 1
            payout = int(bet.amount * odds)
            bet.status = BetStatus.WON
            bet.payout = payout

            # give the cash back to user
            user = bet.user
            try:
                user.balance += payout
            except KeyError:
                print(f"User {user.email} not found while trying to give cash back")

            results.append({"user": user.email, "payout": payout})
        else:
            # losing side
            bet.status = BetStatus.LOST
            bet.payout = 0
            results.append({"user": bet.user.email, "payout": 0})

    # update goal
    goal.status = outcome
    db.commit()
    return results
