# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 20:17

@author: Aidan
@project: GoalBet
@filename: settings
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'GoalBet API'
    env: str = 'local'
    encrypt_algorithm: str = 'HS256'
    secret_key: str = ''
    access_token_expire_minutes: int = 60
    initial_balance: int = 1000
    database_url: str = 'postgresql://goalbet:goalbet@db:5432/goalbet'
    frontend_api_key: str = ''
    frontend_domain: str = ''
    log2file: bool = Field(default=False, alias='LOG2FILE')

    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')


settings = Settings()
