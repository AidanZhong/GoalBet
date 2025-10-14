# -*- coding: utf-8 -*-
"""
Created on 2025/9/29 22:26

@author: Aidan
@project: GoalBet
@filename: routers_stream
"""
from fastapi import APIRouter

from api.app.core.events import sse_stream

router = APIRouter(prefix="/stream", tags=["stream"])


@router.get("")
def stream():
    return sse_stream()
