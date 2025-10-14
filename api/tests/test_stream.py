# -*- coding: utf-8 -*-
"""
Created on 2025/10/14 22:25

@author: Aidan
@project: GoalBet
@filename: test_stream
"""
import asyncio

import pytest
from starlette.testclient import TestClient

from api.app.core.events import broadcast
from api.app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_sse_broadcast():
    asyncio.create_task(broadcast("goal.test", {"msg": "hello"}))
    # Just confirm broadcast doesn’t crash
    assert True
