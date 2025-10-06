# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 20:02

@author: Aidan
@project: GoalBet
@filename: routers_users
@description: 
- Python 
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing_extensions import deprecated

from api.app.api.routers_auth import get_current_user
from api.app.core.db import get_db
from api.app.models.bet import BetPublic
from api.app.models.db_models import User, Bet
from api.app.models.user import UserPublic, UserCreate
from api.app.core import data_store

router = APIRouter(prefix="/users", tags=["users"])


@deprecated("This endpoint is deprecated. Please use /auth/register instead.")
@router.post("/user_create", response_model=UserPublic)
def create_user(user: UserCreate):
    if user.email in data_store._db:
        raise HTTPException(status_code=400, detail="user already exists")

    # update the database
    data_store._user_id = data_store._user_id + 1
    data_store._db[user.email] = {"id": data_store._user_id, "email": user.email}
    return data_store._db[user.email]


@router.get("/bets", response_model=list[BetPublic])
def list_my_bets(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Bet).filter(Bet.user_id == user["id"]).all()
