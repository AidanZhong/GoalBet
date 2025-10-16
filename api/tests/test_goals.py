# -*- coding: utf-8 -*-
"""
Created on 2025/9/29 9:27

@author: Aidan
@project: GoalBet
@filename: test_goals
"""
from datetime import datetime, timedelta, timezone


def test_create_and_list_goal(client):
    # register + login
    r = client.post("/auth/register", json={"email": "g@x.com", "password": "pw123"})
    token = client.post("/auth/login", json={"email": "g@x.com", "password": "pw123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create goal
    payload = {
        "title": "Run a marathon",
        "description": "Complete 42km race",
        "deadline": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
    }
    r = client.post("/goals", json=payload, headers=headers)
    assert r.status_code == 200
    goal = r.json()
    assert goal["title"] == "Run a marathon"

    # list goals
    r = client.get("/goals")
    assert r.status_code == 200
    assert any(g["title"] == "Run a marathon" for g in r.json())

    # fetch single goal
    gid = goal["id"]
    r = client.get(f"/goals/{gid}", headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == gid


def test_update_goal(client):
    # register + login
    r = client.post("/auth/register", json={"email": "g@x.com", "password": "pw123"})
    token = client.post("/auth/login", json={"email": "g@x.com", "password": "pw123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create goal
    payload = {
        "title": "Run a marathon",
        "description": "Complete 42km race",
        "deadline": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
    }
    r = client.post("/goals", json=payload, headers=headers)
    assert r.status_code == 200
    goal = r.json()
    assert goal["title"] == "Run a marathon"

    # post update
    update_payload = {"content": "Finished book 1"}
    r = client.post(f"/goals/{goal['id']}/updates", json=update_payload, headers=headers)
    assert r.status_code == 200
    update = r.json()
    assert update["content"] == "Finished book 1"
    assert update["goal_id"] == goal["id"]

    # fetch goal with updates
    r = client.get(f"/goals/{goal['id']}", headers=headers)
    assert r.status_code == 200
    assert r.json()["updates"][0]["content"] == "Finished book 1"


def test_update_without_token(client):
    r = client.post("/goals/999/updates", json={"content": "Finished book 1"})
    assert r.status_code == 401
