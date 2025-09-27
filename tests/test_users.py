# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 20:12

@author: Aidan
@project: GoalBet
@filename: test_users
@description: 
- Python 
"""
from fastapi.testclient import TestClient
from api.app.main import app


def test_create_users():
    client = TestClient(app)
    response = client.post("/users/user_create", json={"email": "x@y.com", "password": "p"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data and data["email"] == "x@y.com"