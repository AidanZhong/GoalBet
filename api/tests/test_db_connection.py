# -*- coding: utf-8 -*-
"""
Created on 2025/10/5 10:58

@author: Aidan
@project: GoalBet
@filename: test_db_connection
@description: 
- Python 
"""
from api.app.core.db import Session_local, Base, engine
from api.app.models.db_models import User

def test_can_create_user():
    Base.metadata.create_all(bind=engine)
    db = Session_local()
    u = User(email="test@db.com", hashed_password="x", balance=500)
    db.add(u)
    db.commit()
    assert db.query(User).filter_by(email="test@db.com").first() is not None
