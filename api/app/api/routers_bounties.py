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
from sqlalchemy.orm import Session

from api.app.api.routers_auth import get_current_user
from api.app.api.routers_stream import broadcast
from api.app.core.db import get_db
from api.app.models.bounty_missions import BountyPublic, BountyCreate, BountySubmission
from api.app.models.db_models import User, Bounty, Submission

router = APIRouter(prefix="/bounties", tags=["bounties"])


@router.post("", response_model=BountyPublic)
def create_bounty(payload: BountyCreate, user: dict = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user["email"]).first()
    if payload.reward > user_db.balance:
        raise HTTPException(status_code=400, detail="Not enough balance")
    else:
        user_db.balance -= payload.reward

    bounty = Bounty(
        title=payload.title,
        description=payload.description,
        reward=payload.reward,
        deadline=payload.deadline,
        owner_id=user_db.id,
    )

    db.add(bounty)
    db.commit()
    db.refresh(bounty)
    broadcast("bounty.created", {
        "owner_email": user["email"],
        "title": payload.title,
        "description": payload.description,
        "reward": payload.reward,
        "deadline": payload.deadline,
    })
    return bounty


@router.post("/{bid}/submit")
def submit_bounty(bid: int, body: BountySubmission, user: dict = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    bounty = db.query(Bounty).filter(Bounty.id == bid).first()
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    created_time = datetime.now(timezone.utc)
    if bounty.deadline < created_time:
        raise HTTPException(status_code=400, detail="Bounty has expired")
    user_db = db.query(User).filter(User.email == user["email"]).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    submission = Submission(
        proof=body.proof,
        bounty_id=bid,
        user_id=user_db.id,
        created_at=created_time
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    broadcast("bounty.submission", {
        "bounty_id": bid,
        "user_email": user["email"]
    })
    return {"Message": "Submission successful", "Bounty": bounty, "Submission": {
        "user_email": user["email"],
        "proof": body.proof,
        "timestamp": created_time
    }}
