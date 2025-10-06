# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 10:30

@author: Aidan
@project: GoalBet
@filename: test_health
@description: 
- Python 
"""
from fastapi.testclient import TestClient
from api.app.main import app


def test_health():
    c = TestClient(app)
    request = c.get('/health')
    assert request.status_code == 200
    assert request.json()['status'] == 'ok'
