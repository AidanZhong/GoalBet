# -*- coding: utf-8 -*-
"""
Created on 2025/9/29 9:08

@author: Aidan
@project: GoalBet
@filename: goal
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from api.app.models.enums import GoalStatus


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

    model_config = {"from_attributes": True}


class GoalPublic(BaseModel):
    id: int
    owner_email: str
    title: str
    description: Optional[str]
    deadline: datetime
    status: GoalStatus
    markets: List[int] = []
    updates: List[GoalUpdatePublic] = []

    model_config = {"from_attributes": True}
