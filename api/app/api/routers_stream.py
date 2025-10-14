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
from api.app.core.events import sse_stream

router = APIRouter(prefix="/stream", tags=["stream"])


@router.get("")
async def stream():
    return sse_stream()
