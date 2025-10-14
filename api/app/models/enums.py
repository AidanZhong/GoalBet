# -*- coding: utf-8 -*-
"""
Created on 2025/9/29 22:01

@author: Aidan
@project: GoalBet
@filename: enums
"""
from enum import Enum


class GoalStatus(str, Enum):
    ACTIVE = "active"
    SUCCESS = "success"
    FAILED = "failed"


class MarketType(str, Enum):
    SUCCESS = "success"
    FAIL = "fail"
