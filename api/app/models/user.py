# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 20:00

@author: Aidan
@project: GoalBet
@filename: user
@description: 
- Python 
"""
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: int
    email: EmailStr
