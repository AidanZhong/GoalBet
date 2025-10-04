# -*- coding: utf-8 -*-
"""
Created on 2025/10/4 23:10

@author: Aidan
@project: GoalBet
@filename: test_bounty
@description: 
- Python 
"""
from datetime import datetime, timedelta

from starlette.testclient import TestClient

from api.app.main import app
from api.app.models.bet import BetSide


def test_me_bets_and_bounty_flow():
    client = TestClient(app)
    # user
    client.post("/auth/register", json={"email": "me@test.com", "password": "pw"})
    token = client.post("/auth/login", json={"email": "me@test.com", "password": "pw"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create goal + bet
    goal = client.post("/goals", json={"title": "GoalX", "deadline": (datetime.utcnow()+timedelta(days=2)).isoformat()}, headers=headers).json()
    gid = goal["id"]
    client.post(f"/markets/{gid}/bets", json={"side": BetSide.SUCCESS, "amount": 100}, headers=headers)

    # /me/bets should return that bet
    r = client.get("/users/bets", headers=headers)
    assert any(b["goal_id"] == gid for b in r.json())

    # create bounty
    bounty_payload = {"title": "Run 5km", "reward": 50, "deadline": (datetime.utcnow()+timedelta(days=5)).isoformat()}
    bounty = client.post("/bounties", json=bounty_payload, headers=headers).json()
    assert bounty["title"] == "Run 5km"

    # submit proof
    sub = client.post(f"/bounties/{bounty['id']}/submit", json={"proof": "https://proof.img"}, headers=headers)
    assert sub.status_code == 200
