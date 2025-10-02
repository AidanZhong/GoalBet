# -*- coding: utf-8 -*-
"""
Created on 2025/10/2 21:54

@author: Aidan
@project: GoalBet
@filename: bet
@description: 
- Python 
"""
from enum import Enum

from pydantic import BaseModel, Field, EmailStr


class BetSide(str, Enum):
    SUCCESS = "success"
    FAIL = "fail"

class BetCreate(BaseModel):
    side: BetSide
    amount: int = Field(..., gt=0) # greater than zero

class BetPublic(BaseModel):
    id: int
    goal_id: int
    user_email: EmailStr
    side: BetSide
    amount: int
    odds_snapshot: float