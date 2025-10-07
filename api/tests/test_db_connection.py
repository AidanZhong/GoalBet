# -*- coding: utf-8 -*-
"""
Created on 2025/10/5 10:58

@author: Aidan
@project: GoalBet
@filename: test_db_connection
@description: 
- Python 
"""
from uuid import uuid4

from api.app.core.db import Session_local
from api.app.models.db_models import User

def test_can_create_user():
    db = Session_local()  # Use the session provided by the shared test database
    
    # Use a unique email for each test run to avoid conflict
    unique_email = f"test_user_{str(uuid4())}@db.com"  

    # Check if the user already exists (for safety)
    existing_user = db.query(User).filter_by(email=unique_email).first()
    if existing_user is None:
        u = User(email=unique_email, hashed_password="x", balance=500)
        db.add(u)
        db.commit()

    # Assert the user exists in the database
    assert db.query(User).filter_by(email=unique_email).first() is not None
    users = db.query(User).all()
    print([u.email for u in users])
    print(len(users))
