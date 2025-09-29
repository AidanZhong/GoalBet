# -*- coding: utf-8 -*-
"""
Created on 2025/9/29 9:18

@author: Aidan
@project: GoalBet
@filename: routers_goals
@description: 
- Python 
"""
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException

from api.app.api.routers_auth import get_current_user
from api.app.models.goal import GoalPublic, GoalCreate

router = APIRouter(prefix='/goals', tags=['goals'])

# fake dataset
_goals: Dict[int, dict] = {}
_goal_id = 0


@router.post("", response_model=GoalPublic)
def create_goal(payload: GoalCreate, user: dict = Depends(get_current_user)):
    global _goal_id
    _goal_id += 1
    goal = {
        "id": _goal_id,
        "owner_email": user["email"],
        "title": payload.title,
        "description": payload.description,
        "deadline": payload.deadline,
        "status": "ACTIVE",
        "markets": ["SUCCESS", "FAIL"]
    }
    _goals[_goal_id] = goal
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
