# -*- coding: utf-8 -*-
"""
Created on 2025/10/4 22:50

@author: Aidan
@project: GoalBet
@filename: bounty_missions
@description: 
- Python 
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BountyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    reward: int = Field(..., gt=0)
    deadline: datetime


class BountyPublic(BaseModel):
    id: int
    owner_email: str
    title: str
    reward: int
    deadline: datetime
    submissions: list = []


class BountySubmission(BaseModel):
    proof: str


