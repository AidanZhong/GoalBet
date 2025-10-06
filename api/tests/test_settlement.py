# -*- coding: utf-8 -*-
"""
Created on 2025/10/3 9:43

@author: Aidan
@project: GoalBet
@filename: test_settlement
@description: 
- Python 
"""
from datetime import datetime, timedelta
from api.app.models.bet import BetSide, BetStatus


def test_settlement_flow(client):
    # User A
    client.post("/auth/register", json={"email": "a@test.com", "password": "pw"})
    token_a = client.post("/auth/login", json={"email": "a@test.com", "password": "pw"}).json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # User B
    client.post("/auth/register", json={"email": "b@test.com", "password": "pw"})
    token_b = client.post("/auth/login", json={"email": "b@test.com", "password": "pw"}).json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Create goal (owner = A)
    payload = {"title": "Win Settlement", "deadline": (datetime.utcnow() + timedelta(days=2)).isoformat()}
    goal = client.post("/goals", json=payload, headers=headers_a).json()
    gid = goal["id"]

    # Bets: A=SUCCESS(100), B=FAIL(100)
    client.post(f"/markets/{gid}/bets", json={"side": BetSide.SUCCESS, "amount": 100}, headers=headers_a)
    client.post(f"/markets/{gid}/bets", json={"side": BetSide.FAIL, "amount": 100}, headers=headers_b)

    # Resolve SUCCESS
    r = client.post(f"/goals/{gid}/resolve", json={"outcome": BetSide.SUCCESS}, headers=headers_a)
    assert r.status_code == 200
    data = r.json()
    assert data["outcome"] == BetSide.SUCCESS

    # Check winner payout
    bets = client.get(f"/markets/{gid}/bets").json()
    for b in bets:
        if b["side"] == BetSide.SUCCESS:
            assert b["status"] == BetStatus.WON
            assert b["payout"] > 100
        else:
            assert b["status"] == BetStatus.LOST
            assert b["payout"] == 0

    # Wallet check: A’s balance should have increased
    after_a = client.get("/wallet", headers=headers_a).json()["balance"]
    assert after_a > 1000  # started with 1000
