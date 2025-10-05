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
    encrypt_algorithm: str = 'HS256'
    secret_key: str = 'dev-secret-key'
    access_token_expire_minutes: int = 60
    initial_balance: int = 1000
    database_url: str = 'sqlite:///./goalbet.db'


settings = Settings()
