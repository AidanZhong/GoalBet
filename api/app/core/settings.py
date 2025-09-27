# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 20:17

@author: Aidan
@project: GoalBet
@filename: settings
@description: 
- Python 
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'GoalBet API'
    env: str = 'local'


settings = Settings()
