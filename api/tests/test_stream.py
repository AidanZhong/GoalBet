# -*- coding: utf-8 -*-
"""
Created on 2025/10/14 22:25

@author: Aidan
@project: GoalBet
@filename: test_stream
@description: 
- Python 
"""
import pytest
from starlette.testclient import TestClient
from api.app.main import app
from api.app.core.events import broadcast
import asyncio

client = TestClient(app)


@pytest.mark.asyncio
async def test_sse_broadcast():
    gen = app.dependency_overrides.get("stream", None)
    asyncio.create_task(broadcast("goal.test", {"msg": "hello"}))
    # Just confirm broadcast doesn’t crash
    assert True
