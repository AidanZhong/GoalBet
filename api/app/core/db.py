# -*- coding: utf-8 -*-
"""
Created on 2025/10/5 10:02

@author: Aidan
@project: GoalBet
@filename: db
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.app.core.settings import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
print("🔗 Connected to:", engine.url)
Session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()
