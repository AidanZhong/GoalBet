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

from fastapi import APIRouter
from sse_starlette import EventSourceResponse

router = APIRouter(prefix="/stream", tags=["stream"])

# simple pub-sub in memory
subscribers = []


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
    for q in subscribers:
        q.put_nowait({"event": event, "data": payload})
