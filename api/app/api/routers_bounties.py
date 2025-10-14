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
from api.app.core.db import get_db
from api.app.models.bounty_missions import BountyPublic, BountyCreate, BountySubmission
from api.app.models.db_models import User, Bounty, Submission
from api.app.service import bounty_service

router = APIRouter(prefix="/bounties", tags=["bounties"])


@router.post("", response_model=BountyPublic)
def create_bounty(payload: BountyCreate, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    bounty = bounty_service.bounty_creation(payload, user, db)
    return BountyPublic.model_validate(bounty)


@router.post("/{bid}/submit")
def submit_bounty(bid: int, body: BountySubmission, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    bounty = db.query(Bounty).filter(Bounty.id == bid).first()
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    created_time = datetime.now(timezone.utc)
    bounty_service.bounty_submission(body, user, bid, db, created_time)
    return {"Message": "Submission successful", "Bounty": bounty, "Submission": {
        "user_email": user.email,
        "proof": body.proof,
        "timestamp": created_time
    }}
