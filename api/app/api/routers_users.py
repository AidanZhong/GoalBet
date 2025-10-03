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
from api.app.core import data_store

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/user_create", response_model=UserPublic)
def create_user(user: UserCreate):
    if user.email in data_store._db:
        raise HTTPException(status_code=400, detail="user already exists")

    #update the database
    data_store._user_id = data_store._user_id + 1
    data_store._db[user.email] = {"id": data_store._user_id, "email": user.email}
    return data_store._db[user.email]