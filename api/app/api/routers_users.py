# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 20:02

@author: Aidan
@project: GoalBet
@filename: routers_users
@description: 
- Python 
"""
from fastapi import APIRouter, HTTPException

from api.app.models.user import UserPublic, UserCreate

router = APIRouter(prefix="/users", tags=["users"])
_db = {}
_id = 0

@router.post("/user_create", response_model=UserPublic)
def create_user(user: UserCreate):
    global _id
    if user.email in _db:
        raise HTTPException(status_code=400, detail="user already exists")

    #update the database
    _id = _id + 1
    _db[user.email] = {"id": _id, "email": user.email}
    return _db[user.email]