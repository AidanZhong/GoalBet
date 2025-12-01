# -*- coding: utf-8 -*-
"""
Created on 2025/9/28 21:55

@author: Aidan
@project: GoalBet
@filename: test_auth_and_wallet
"""
import re


def extract_token_from_email(body: str) -> str:
    """
    Email body contains .../verify?token=<TOKEN> or .../reset?token=<TOKEN>
    Extract URL-safe token.
    """
    m = re.search(r"token=([A-Za-z0-9_-]+)(?=\.|$)", body or "")
    assert m, f"Token not found in email body: {body}"
    return m.group(1)


def test_register_and_login(client, captured_email):
    # register
    r = client.post("/auth/register", json={"email": "a@b.com", "password": "pw123"})
    assert r.status_code == 200
    user = r.json()
    assert user["email"] == "a@b.com"

    # login should fail without email verification
    r = client.post("/auth/login", json={"email": "a@b.com", "password": "pw123"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Email not verified"

    # Re-send verification (captures email, we parse token)
    r = client.post("/auth/verify/resend", json={"email": "a@b.com"})
    assert r.status_code == 200
    verify_token = extract_token_from_email(captured_email['body'])

    # verify email
    r = client.get("/auth/verify", params={"token": verify_token})
    assert r.status_code == 200

    # login with email and password
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
