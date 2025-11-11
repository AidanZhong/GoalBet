# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 10:23

@author: Aidan
@project: GoalBet
@filename: main.py
"""
import time
import traceback
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
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
from api.app.core.logger import get_logger
from api.app.core.settings import settings

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title=settings.app_name)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

logger = get_logger()
logger.info("Starting GoalBet API...")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        trace_id = str(uuid.uuid4())[:8]
        start = time.time()
        response = await call_next(request)
        process_time = (time.time() - start) * 1000
        logger.info(
            f"[trace={trace_id}] {request.method} {request.url.path}"
            f"-> {response.status_code} in {process_time:.2f}ms"
        )
        response.headers["X-Trace-ID"] = trace_id
        return response


app.add_middleware(RequestLoggingMiddleware)


@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    trace_id = getattr(request.state, "trace_id", "no-trace")
    try:
        response = await call_next(request)
        # Only log details for 4xx or 5xx
        if response.status_code >= 400:
            resp_type = type(response).__name__
            # 尝试以安全方式获取响应体，避免访问不存在的属性或消耗流
            body_preview = "<non-readable body>"
            try:
                # starlette Response 在渲染后常带有私有属性 .body（bytes）
                raw = getattr(response, "body", None)
                if isinstance(raw, (bytes, bytearray)):
                    body_preview = raw.decode("utf-8", errors="replace")
                else:
                    # 某些 JSONResponse 拥有 .media 可序列化
                    media = getattr(response, "media", None)
                    if media is not None:
                        body_preview = str(media)
                    else:
                        # 最后再尝试 .render()（不要对 StreamingResponse 调用）
                        from starlette.responses import Response as StarletteResponse, StreamingResponse

                        if isinstance(response, StarletteResponse) and not isinstance(response, StreamingResponse):
                            rendered = response.render(response.body if hasattr(response, "body") else None)
                            if isinstance(rendered, (bytes, bytearray)):
                                body_preview = rendered.decode("utf-8", errors="replace")
                            else:
                                body_preview = str(rendered)
            except Exception:
                # 安全兜底：不让日志失败影响响应
                pass
            logger.error(
                f"[trace={trace_id}] {request.method} {request.url.path} {resp_type} {response.status_code}: "
                f"{body_preview}"
            )
        return response
    except Exception as e:
        logger.error(f"[trace={trace_id}] {request.method} {request.url.path} crashed: {e}\n" + traceback.format_exc())
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


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
    allow_origins=[settings.frontend_domain, 'https://goalbet.dev', 'https://www.goalbet.dev', 'http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
