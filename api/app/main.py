# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 10:23

@author: Aidan
@project: GoalBet
@filename: main.py
"""
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.cors import CORSMiddleware

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

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title=settings.app_name)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.on_event("startup")
async def on_startup() -> None:
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

# CORS restriction
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_domain],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
