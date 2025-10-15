# -*- coding: utf-8 -*-
"""
Created on 2025/10/5 10:58

@author: Aidan
@project: GoalBet
@filename: test_db_connection
"""
from uuid import uuid4

from api.app.core.db import get_db
from api.app.main import app
from api.app.models.db_models import User


def test_can_create_user():
    # 通过覆盖依赖拿到一个测试会话
    override = app.dependency_overrides[get_db]
    gen = override()
    db = next(gen)
    try:
        unique_email = f"test_user_{uuid4()}@db.com"
        assert db.query(User).filter_by(email=unique_email).first() is None
        db.add(User(email=unique_email, hashed_password="x", balance=500))
        db.commit()
        assert db.query(User).filter_by(email=unique_email).first() is not None
    finally:
        try:
            next(gen)  # 触发 generator 的 finally 关闭 db
        except StopIteration:
            pass
