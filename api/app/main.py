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


class Settings(BaseSettings):
    app_name: str = 'GoalBet API'
    env: str = 'local'


settings = Settings()
app = FastAPI(title=settings.app_name)


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.env}
