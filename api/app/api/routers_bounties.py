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
def create_bounty(payload: BountyCreate, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    if payload.reward > user.balance:
        raise HTTPException(status_code=400, detail="Not enough balance")
    else:
        user.balance -= payload.reward

    bounty = Bounty(
        title=payload.title,
        description=payload.description,
        reward=payload.reward,
        deadline=payload.deadline,
        owner_id=user.id,
    )

    db.add(bounty)
    db.commit()
    db.refresh(bounty)
    broadcast("bounty.created", {
        "owner_email": user.email,
        "title": payload.title,
        "description": payload.description,
        "reward": payload.reward,
        "deadline": payload.deadline,
    })
    return BountyPublic.model_validate(bounty)


@router.post("/{bid}/submit")
def submit_bounty(bid: int, body: BountySubmission, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    bounty = db.query(Bounty).filter(Bounty.id == bid).first()
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    
    created_time = datetime.now(timezone.utc)
    # Convert `bounty.deadline` to a timezone-aware datetime, assuming it's UTC
    if bounty.deadline.tzinfo is None:
        bounty_deadline_aware = bounty.deadline.replace(tzinfo=timezone.utc)
    else:
        bounty_deadline_aware = bounty.deadline

    if bounty_deadline_aware < created_time:
        raise HTTPException(status_code=400, detail="Bounty has expired")
    
    submission = Submission(
        proof=body.proof,
        bounty_id=bid,
        user_id=user.id,
        created_at=created_time
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    broadcast("bounty.submission", {
        "bounty_id": bid,
        "user_email": user.email
    })
    return {"Message": "Submission successful", "Bounty": bounty, "Submission": {
        "user_email": user.email,
        "proof": body.proof,
        "timestamp": created_time
    }}
