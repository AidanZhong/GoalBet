# -*- coding: utf-8 -*-
"""
Created on 2025/10/2 22:20

@author: Aidan
@project: GoalBet
@filename: test_bets
"""
from datetime import datetime, timedelta

from api.app.models.bet import BetSide
from api.tests.test_auth_and_wallet import extract_token_from_email


def test_place_bet_and_wallet_deduction(client, captured_email):
    # user setup
    client.post("/auth/register", json={"email": "bet@x.com", "password": "pw"})
    # Re-send verification (captures email, we parse token)
    r = client.post("/auth/verify/resend", json={"email": "a@b.com"})
    assert r.status_code == 200
    verify_token = extract_token_from_email(captured_email['body'])

    # verify email
    r = client.get("/auth/verify", params={"token": verify_token})
    assert r.status_code == 200
    token = client.post("/auth/login", json={"email": "bet@x.com", "password": "pw"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create goal
    payload = {
        "title": "Test Bet Goal",
        "deadline": (datetime.utcnow() + timedelta(days=2)).isoformat(),
    }
    gid = client.post("/goals", json=payload, headers=headers).json()["id"]

    # check wallet before
    before = client.get("/wallet", headers=headers).json()["balance"]

    # place bet
    bet_payload = {"side": BetSide.SUCCESS, "amount": 100}
    r = client.post(f"/markets/{gid}/bets", json=bet_payload, headers=headers)
    assert r.status_code == 200
    bet = r.json()
    assert bet["goal_id"] == gid
    assert bet["amount"] == 100
    assert "odds_snapshot" in bet

    # wallet decreased
    after = client.get("/wallet", headers=headers).json()["balance"]
    assert after == before - 100


def test_cannot_bet_without_balance(client, captured_email):
    client.post("/auth/register", json={"email": "poor@x.com", "password": "pw"})
    # Re-send verification (captures email, we parse token)
    r = client.post("/auth/verify/resend", json={"email": "a@b.com"})
    assert r.status_code == 200
    verify_token = extract_token_from_email(captured_email['body'])

    # verify email
    r = client.get("/auth/verify", params={"token": verify_token})
    assert r.status_code == 200
    token = client.post("/auth/login", json={"email": "poor@x.com", "password": "pw"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create goal
    payload = {
        "title": "Impossible Bet",
        "deadline": (datetime.utcnow() + timedelta(days=1)).isoformat(),
    }
    gid = client.post("/goals", json=payload, headers=headers).json()["id"]

    # bet more than balance
    r = client.post(f"/markets/{gid}/bets", json={"side": BetSide.FAIL, "amount": 999999}, headers=headers)
    assert r.status_code == 400
