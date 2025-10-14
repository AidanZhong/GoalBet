# -*- coding: utf-8 -*-
"""
Created on 2025/9/28 21:55

@author: Aidan
@project: GoalBet
@filename: test_auth_and_wallet
"""


def test_register_and_login(client):
    # register
    r = client.post("/auth/register", json={"email": "a@b.com", "password": "pw123"})
    assert r.status_code == 200
    user = r.json()
    assert user["email"] == "a@b.com"

    # login
    r = client.post("/auth/login", json={"email": "a@b.com", "password": "pw123"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token

    # /me with token
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["email"] == "a@b.com"

    # wallet
    r = client.get("/wallet", headers=headers)
    assert r.status_code == 200
    assert "balance" in r.json()
