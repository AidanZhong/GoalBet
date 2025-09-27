# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 10:23

@author: Aidan
@project: GoalBet
@filename: main.py
@description: 
- Python 
"""
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from api.app.api.routers_health import router as health_router
from api.app.api.routers_users import router as users_router
from api.app.core.settings import settings

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(users_router)
