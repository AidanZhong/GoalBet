# -*- coding: utf-8 -*-
"""
Created on 2025/9/29 9:18

@author: Aidan
@project: GoalBet
@filename: routers_goals
@description: 
- Python 
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.app.api.routers_auth import get_current_user
from api.app.api.routers_stream import broadcast
from api.app.models.db_models import Goal, GoalUpdate, Bet, User
from api.app.models.enums import GoalStatus, MarketType
from api.app.models.goal import GoalPublic, GoalCreate, GoalUpdatePublic, GoalUpdateCreate
from api.app.service import goal_service
from api.app.service.settlement import resolve_market
from api.app.core.db import get_db

router = APIRouter(prefix='/goals', tags=['goals'])


@router.post("", response_model=GoalPublic)
def create_goal(payload: GoalCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = goal_service.create_goal(payload, user, db)
    return GoalPublic.model_validate(goal)


@router.get("", response_model=list[GoalPublic])
def list_goals(db: Session = Depends(get_db)):
    return [GoalPublic.model_validate(g) for g in goal_service.get_all_goals(db)]


@router.get("/{goal_id}", response_model=GoalPublic)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = goal_service.get_goal(goal_id, db)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return GoalPublic.model_validate(goal)


@router.post("/{goal_id}/updates", response_model=GoalUpdatePublic)
def post_update(goal_id: int, payload: GoalUpdateCreate, user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    update = goal_service.update_goal(goal_id, payload, user, db)
    return GoalUpdatePublic.model_validate(update)


@router.post("/{goal_id}/resolve")
def resolve_goal(goal_id: int, outcome: str = Body(..., embed=True),
                 user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = goal_service.get_goal(goal_id, db)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal.owner.email != user.email:
        # maybe changed some day
        raise HTTPException(status_code=403, detail="Only owner can resolve goal")

    results = resolve_market(goal_id, outcome, db)
    data = {
        "goal_id": goal_id,
        "outcome": outcome,
        "results": results
    }
    broadcast("market settled", data)
    return data


@router.get("/trending", response_model=list[GoalPublic])
def trending_goals(db: Session = Depends(get_db)):
    goals = goal_service.get_goal_trends(db)
    return [GoalPublic.model_validate(g) for g in goals]


@router.get("/mine", response_model=list[GoalPublic])
def list_my_goals(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return [GoalPublic.model_validate(g) for g in goal_service.list_user_goals(user, db)]
