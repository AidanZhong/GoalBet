# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 18:09

@author: Aidan
@project: GoalBet
@filename: routers_health
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from api.app.core.db import get_db
from api.app.core.logger import get_logger

router = APIRouter()
logger = get_logger()


@router.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected", "version": "1.0.1"}
    except Exception as e:
        logger.error(e)
        return {"status": "error", "db": str(e)}
