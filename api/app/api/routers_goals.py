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
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException

from api.app.api.routers_auth import get_current_user
from api.app.api.routers_stream import broadcast
# 在创建/更新目标后，广播事件时，确保传入的 payload 仅包含可 JSON 序列化的基本类型（如将 datetime 转换为 isoformat 字符串）。
# 例如：
# broadcast("goal_created", {"id": goal.id, "title": goal.title, "deadline": goal.deadline.isoformat()})
# 或对于更新：
# broadcast("goal_updated", {"id": goal.id, "updated_at": updated_at.isoformat()})
from api.app.models.enums import GoalStatus, MarketType
from api.app.models.goal import GoalPublic, GoalCreate, GoalUpdatePublic, GoalUpdateCreate

router = APIRouter(prefix='/goals', tags=['goals'])

# fake dataset
_goals: Dict[int, dict] = {}
_goal_id = 0
_updates: Dict[int, list] = {}
_update_id = 0


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

    global _goal_id
    _goal_id += 1
    goal = {
        "id": _goal_id,
        "owner_email": user["email"],
        "title": payload.title,
        "description": payload.description,
        "deadline": deadline,
        "status": GoalStatus.ACTIVE,
        "markets": [MarketType.SUCCESS, MarketType.FAIL],
        "updates": []
    }
    _goals[_goal_id] = goal
    _updates[_goal_id] = []

    broadcast("goal.created", goal)
    return goal


@router.get("", response_model=list[GoalPublic])
def list_goals():
    return list(_goals.values())


@router.get("/{goal_id}", response_model=GoalPublic)
def get_goal(goal_id: int):
    goal = _goals.get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.post("/{goal_id}/updates", response_model=GoalUpdatePublic)
def post_update(goal_id: int, payload: GoalUpdateCreate, user: dict = Depends(get_current_user)):
    goal = _goals.get(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal["owner_email"] != user["email"]:
        raise HTTPException(status_code=403, detail="Only owner can post updates")

    global _update_id
    _update_id += 1
    update = {
        "id": _update_id,
        "goal_id": goal_id,
        "content": payload.content,
        "author_email": user["email"],
        "created_at": datetime.now(timezone.utc)
    }
    _updates[goal_id].append(update)
    goal["updates"].append(update)

    broadcast("goal.update", update)
    return update
