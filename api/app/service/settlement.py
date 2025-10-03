# -*- coding: utf-8 -*-
"""
Created on 2025/10/3 9:25

@author: Aidan
@project: GoalBet
@filename: settlement
@description: 
- Python 
"""
from fastapi import HTTPException
from api.app.models.bet import BetStatus
from api.app.core import data_store
from api.app.models.enums import GoalStatus


def resolve_market(goal_id: int, outcome: str):
    if goal_id not in data_store._goals:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal_id not in data_store._bets:
        raise HTTPException(status_code=404, detail="Bet not found")

    total_pool = sum(data_store._pools[goal_id].values())
    winning_pool = data_store._pools[goal_id].get(outcome, 0)

    results = []
    for bet in data_store._bets[goal_id]:
        if bet["side"] == outcome:
            # winning side
            odds = total_pool / winning_pool if winning_pool > 0 else 1
            payout = int(bet["amount"] * odds)
            bet["status"] = BetStatus.WON
            bet["payout"] = payout

            # give the cash back to user
            user_email = bet["user_email"]
            try:
                data_store._db[user_email]["balance"] += payout
            except KeyError:
                print(f"User {user_email} not found while trying to give cash back")

            results.append({"user": user_email, "payout": payout})
        else:
            # losing side
            bet["status"] = BetStatus.LOST
            bet["payout"] = 0
            results.append({"user": bet["user_email"], "payout": 0})

    # update goal
    goal = data_store._goals[goal_id]
    goal["status"] = outcome
    return results
