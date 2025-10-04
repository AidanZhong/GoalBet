# -*- coding: utf-8 -*-
"""
Created on 2025/10/4 22:52

@author: Aidan
@project: GoalBet
@filename: routers_bounties
@description: 
- Python 
"""
from datetime import timezone, datetime

from fastapi import APIRouter, Depends, HTTPException

from api.app.api.routers_auth import get_current_user
from api.app.api.routers_stream import broadcast
from api.app.core import data_store
from api.app.models.bounty_missions import BountyPublic, BountyCreate, BountySubmission

router = APIRouter(prefix="/bounties", tags=["bounties"])


@router.post("", response_model=BountyPublic)
def create_bounty(payload: BountyCreate, user: dict = Depends(get_current_user)):
    if payload.reward > user["balance"]:
        raise HTTPException(status_code=400, detail="Not enough balance")
    else:
        user["balance"] -= payload.reward

    data_store._bounty_mission_id += 1
    bid = data_store._bounty_mission_id

    bounty = {
        "id": bid,
        "owner_email": user["email"],
        "title": payload.title,
        "description": payload.description,
        "reward": payload.reward,
        "deadline": payload.deadline,
        "submissions": []
    }
    data_store._bounty_missions[bid] = bounty
    data_store._bounty_mission_submissions[bid] = []
    broadcast("bounty.created", bounty)
    return bounty


@router.post("/{bid}/submit")
def submit_bounty(bid: int, body: BountySubmission, user: dict = Depends(get_current_user)):
    bounty = data_store._bounty_missions.get(bid)
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    sub = {
        "user_email": user["email"],
        "proof": body.proof,
        "timestamp": datetime.now(timezone.utc)
    }
    data_store._bounty_mission_submissions[bid].append(sub)
    broadcast("bounty.submission", {
        "bounty_id": bid,
        "user_email": user["email"]
    })
    return {"Message": "Submission successful", "Bounty": bounty, "Submission": sub}
