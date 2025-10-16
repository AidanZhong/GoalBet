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

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from api.app.api.routers_auth import get_current_user
from api.app.core.db import get_db
from api.app.core.security import verify_frontend_key
from api.app.models.bet import BetCreate, BetPublic
from api.app.models.db_models import User
from api.app.service import bet_service

router = APIRouter(prefix="/markets", tags=["bets"])


@router.post("/{goal_id}/bets", response_model=BetPublic, dependencies=[Depends(verify_frontend_key)])
def place_bet(
    goal_id: int,
    payload: BetCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    bet = bet_service.place_bet(db, goal_id, payload, user, background_tasks)
    betPublic = BetPublic.model_validate(bet)
    return betPublic


@router.get("/{goal_id}/bets", response_model=List[BetPublic], dependencies=[Depends(verify_frontend_key)])
def list_bets(goal_id: int, db: Session = Depends(get_db)):
    return [BetPublic.model_validate(b) for b in bet_service.get_bets(db, goal_id)]
