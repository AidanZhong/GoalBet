# -*- coding: utf-8 -*-
"""
Created on 2025/9/27 18:09

@author: Aidan
@project: GoalBet
@filename: routers_health
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}
