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
from api.app.models.db_models import Goal, GoalUpdate, Bet
from api.app.models.enums import GoalStatus, MarketType
from api.app.models.goal import GoalPublic, GoalCreate, GoalUpdatePublic, GoalUpdateCreate
from api.app.service.settlement import resolve_market
from api.app.core.db import get_db

router = APIRouter(prefix='/goals', tags=['goals'])


@router.post("", response_model=GoalPublic)
def create_goal(payload: GoalCreate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # 统一将 deadline 归一化为 UTC aware datetime
    deadline = payload.deadline
    if deadline.tzinfo is None:
        # 视为 UTC
        deadline = deadline.replace(tzinfo=timezone.utc)
    else:
        # 转换为 UTC
        deadline = deadline.astimezone(timezone.utc)

    if deadline <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Goal deadline must be in the future")

    goal = Goal(
        title=payload.title,
        description=payload.description,
        deadline=payload.deadline,
        status=GoalStatus.ACTIVE,
    )

    db.add(goal)
    db.commit()
    db.refresh(goal)

    broadcast("goal.created", {"id": goal.id, "title": goal.title})
    return goal


@router.get("", response_model=list[GoalPublic])
def list_goals(db: Session = Depends(get_db)):
    return db.query(Goal).all()


@router.get("/{goal_id}", response_model=GoalPublic)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.post("/{goal_id}/updates", response_model=GoalUpdatePublic)
def post_update(goal_id: int, payload: GoalUpdateCreate, user: dict = Depends(get_current_user),
                db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal["owner_email"] != user["email"]:
        raise HTTPException(status_code=403, detail="Only owner can post updates")

    update = GoalUpdate(
        goal_id=goal_id,
        content=payload.content,
        author_id=user["id"],
        created_at=datetime.now(timezone.utc)
    )
    db.add(update)
    db.commit()
    db.refresh(update)

    broadcast("goal.update", {
        "goal updated": goal_id,
        "update id": update.id,
    })
    return update


@router.post("/{goal_id}/resolve")
def resolve_goal(goal_id: int, outcome: str = Body(..., embed=True),
                 user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal.owner.email != user["email"]:
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
    # ranked by price pool
    # Compute total pool for each goal
    pool_subquery = (
        db.query(
            Bet.goal_id,
            func.coalesce(func.sum(Bet.amount), 0).label("total_pool")
        )
        .group_by(Bet.goal_id)
        .subquery()
    )
    # join goals with their pools
    query = (
        db.query(Goal)
        .outerjoin(pool_subquery, Goal.id == pool_subquery.c.goal_id)
        .order_by(pool_subquery.c.total_pool.desc().nullslast())
    )

    goals = query.all()
    return goals


@router.get("/mine", response_model=list[GoalPublic])
def list_my_goals(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Goal).filter(Goal.owner_id == user["id"]).all()
