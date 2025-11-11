# -*- coding: utf-8 -*-
"""
Created on 11/11/2025 22:39

@author: Aidan
@project: GoalBet
@filename: bootstrap_db.py
"""
from api.app.core.db import Base, engine

# Import ALL model modules so they register with Base
from api.app.models import db_models

print("Creating tables on", engine.url)
print(db_models)
Base.metadata.create_all(bind=engine)
print("Done.")
