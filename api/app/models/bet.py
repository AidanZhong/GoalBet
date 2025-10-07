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
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class BetSide(str, Enum):
    SUCCESS = "success"
    FAIL = "fail"


class BetStatus(str, Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"


class BetCreate(BaseModel):
    side: BetSide
    amount: int = Field(..., gt=0)  # greater than zero


class BetPublic(BaseModel):
    id: int
    goal_id: int
    user_email: EmailStr
    side: BetSide
    amount: int
    odds_snapshot: float
    status: BetStatus
    payout: Optional[int] = None

    model_config = {"from_attributes": True}
