# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 10:23

@author: Aidan
@project: GoalBet
@filename: main.py
"""
from fastapi import FastAPI

from api.app.api.routers_auth import router as auth_router
from api.app.api.routers_bets import router as bets_router
from api.app.api.routers_bounties import router as bounties_router
from api.app.api.routers_goals import router as goals_router
from api.app.api.routers_health import router as health_router
from api.app.api.routers_stream import router as stream_router
from api.app.api.routers_users import router as users_router
from api.app.api.routers_wallet import router as wallet_router
from api.app.core.db import Base, engine
from api.app.core.settings import settings

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
async def on_startup() -> None:
    # 仅在 SQLite（通常是测试场景）下创建表；生产/开发请用 Alembic 迁移
    try:
        url = str(engine.url)
    except Exception:
        url = ""
    if url.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)


app.include_router(health_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(wallet_router)
app.include_router(goals_router)
app.include_router(stream_router)
app.include_router(bets_router)
app.include_router(bounties_router)
