# -*- coding: utf-8 -*-
"""
Created on 2025/9/29 22:26

@author: Aidan
@project: GoalBet
@filename: routers_stream
@description: 
- Python 
"""
import asyncio
import json
from datetime import datetime, date
from typing import Any

from fastapi import APIRouter
from sse_starlette import EventSourceResponse
from api.app.core.data_store import _subscribers as subscribers

router = APIRouter(prefix="/stream", tags=["stream"])



async def event_generator():
    q = asyncio.Queue()
    subscribers.append(q)
    try:
        while True:
            event = await q.get()
            yield {"event": "update", "data": json.dumps(event)}
    finally:
        subscribers.remove(q)


@router.get("")
async def stream():
    return EventSourceResponse(event_generator())


def broadcast(event: str, payload: dict):
    safe_payload = to_jsonable(payload)
    for q in subscribers:
        q.put_nowait({"event": event, "data": safe_payload})


def to_jsonable(obj: Any):
    # 递归将对象转换为可 JSON 序列化的基本类型
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    if isinstance(obj, (datetime, date)):
        # 统一使用 ISO8601 字符串
        return obj.isoformat()
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [to_jsonable(x) for x in obj]
    # 兜底：转字符串，避免抛错（更推荐在上游控制类型）
    return str(obj)
