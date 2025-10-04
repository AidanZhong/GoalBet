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

from api.app.api.routers_auth import get_current_user
from api.app.api.routers_stream import broadcast
from api.app.models.enums import GoalStatus, MarketType
from api.app.models.goal import GoalPublic, GoalCreate, GoalUpdatePublic, GoalUpdateCreate
from api.app.service.settlement import resolve_market
from api.app.core import data_store

router = APIRouter(prefix='/goals', tags=['goals'])


@router.post("", response_model=GoalPublic)
def create_goal(payload: GoalCreate, user: dict = Depends(get_current_user)):
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

    data_store._goal_id += 1
    goal = {
        "id": data_store._goal_id,
        "owner_email": user["email"],
        "title": payload.title,
        "description": payload.description,
        "deadline": deadline,
        "status": GoalStatus.ACTIVE,
        "markets": [MarketType.SUCCESS, MarketType.FAIL],
        "updates": []
    }
    data_store._goals[data_store._goal_id] = goal
    data_store._updates[data_store._goal_id] = []

    broadcast("goal.created", goal)
    return goal


@router.get("", response_model=list[GoalPublic])
def list_goals():
    return list(data_store._goals.values())


@router.get("/{goal_id}", response_model=GoalPublic)
def get_goal(goal_id: int):
    goal = data_store._goals.get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.post("/{goal_id}/updates", response_model=GoalUpdatePublic)
def post_update(goal_id: int, payload: GoalUpdateCreate, user: dict = Depends(get_current_user)):
    goal = data_store._goals.get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal["owner_email"] != user["email"]:
        raise HTTPException(status_code=403, detail="Only owner can post updates")

    data_store._update_id += 1
    update = {
        "id": data_store._update_id,
        "goal_id": goal_id,
        "content": payload.content,
        "author_email": user["email"],
        "created_at": datetime.now(timezone.utc)
    }
    data_store._updates[goal_id].append(update)
    goal["updates"].append(update)

    broadcast("goal.update", update)
    return update


@router.post("/{goal_id}/resolve")
def resolve_goal(goal_id: int, outcome: str = Body(..., embed=True), user: dict = Depends(get_current_user)):
    goal = data_store._goals.get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal["owner_email"] != user["email"]:
        # maybe changed some day
        raise HTTPException(status_code=403, detail="Only owner can resolve goal")

    results = resolve_market(goal_id, outcome)
    data = {
        "goal_id": goal_id,
        "outcome": outcome,
        "results": results
    }
    broadcast("market settled", data)
    return data


@router.get("/trending", response_model=list[GoalPublic])
def trending_goals():
    # ranked by price pool
    goals = sorted(data_store._goals.values(),
                   key=lambda g: sum(data_store._pools.get(g["id"], {}).values()),
                   reverse=True)
    return goals


@router.get("/mine", response_model=list[GoalPublic])
def list_my_goals(user: dict = Depends(get_current_user)):
    return [g for g in data_store._goals.values() if g["owner_email"] == user["email"]]
