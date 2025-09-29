# -*- coding: utf-8 -*-
"""
Created on 2025/9/29 9:27

@author: Aidan
@project: GoalBet
@filename: test_goals
@description: 
- Python 
"""
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from api.app.main import app


def test_create_and_list_goal():
    client = TestClient(app)
    # register + login
    r = client.post("/auth/register", json={"email": "g@x.com", "password": "pw123"})
    token = client.post("/auth/login", json={"email": "g@x.com", "password": "pw123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create goal
    payload = {
        "title": "Run a marathon",
        "description": "Complete 42km race",
        "deadline": (datetime.utcnow() + timedelta(days=7)).isoformat()
    }
    r = client.post("/goals", json=payload, headers=headers)
    assert r.status_code == 200
    goal = r.json()
    assert goal["title"] == "Run a marathon"
    assert "SUCCESS" in goal["markets"]

    # list goals
    r = client.get("/goals")
    assert r.status_code == 200
    assert any(g["title"] == "Run a marathon" for g in r.json())

    # fetch single goal
    gid = goal["id"]
    r = client.get(f"/goals/{gid}")
    assert r.status_code == 200
    assert r.json()["id"] == gid
