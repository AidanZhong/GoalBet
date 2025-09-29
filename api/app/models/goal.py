# -*- coding: utf-8 -*-
"""
Created on 2025/9/29 9:08

@author: Aidan
@project: GoalBet
@filename: goal
@description: 
- Python 
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr


class GoalCreate(BaseModel):
    title: str = Field(..., max_length=100)  # ... means that the field is required
    description: Optional[str] = None
    deadline: datetime


class GoalUpdateCreate(BaseModel):
    content: str = Field(..., max_length=10000)


class GoalUpdatePublic(BaseModel):
    id: int
    goal_id: int
    content: str
    author_email: EmailStr
    created_at: datetime


class GoalPublic(BaseModel):
    id: int
    owner_email: str
    title: str
    description: Optional[str]
    deadline: datetime
    status: str
    markets: List[str] = []
    updates: List[GoalUpdatePublic] = []
