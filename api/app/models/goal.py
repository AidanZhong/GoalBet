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
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    deadline: datetime
    youtube_url: Optional[str] = None


class GoalUpdateCreate(BaseModel):
    content: str = Field(..., max_length=10000)
    youtube_url: Optional[str] = None


class GoalUpdatePublic(BaseModel):
    id: int
    goal_id: int
    content: str
    author_email: EmailStr
    created_at: datetime
    youtube_url: Optional[str] = None

    model_config = {"from_attributes": True}


class GoalPatch(BaseModel):
    youtube_url: Optional[str] = None


class CommentCreate(BaseModel):
    content: str = Field(..., max_length=2000)


class CommentPublic(BaseModel):
    id: int
    goal_id: int
    content: str
    author_email: str
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
    comments: List[CommentPublic] = []
    youtube_url: Optional[str] = None

    model_config = {"from_attributes": True}
