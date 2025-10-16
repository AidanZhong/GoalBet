# -*- coding: utf-8 -*-
"""
Created on 2025/10/4 22:52

@author: Aidan
@project: GoalBet
@filename: routers_bounties
"""
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from api.app.api.routers_auth import get_current_user
from api.app.core.db import get_db
from api.app.core.security import verify_frontend_key
from api.app.models.bounty_missions import BountyCreate, BountyPublic, BountySubmission
from api.app.models.db_models import Bounty, User
from api.app.service import bounty_service

router = APIRouter(prefix="/bounties", tags=["bounties"])

limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=BountyPublic, dependencies=[Depends(verify_frontend_key)])
@limiter.limit("10/minute")
def create_bounty(
    request: Request,
    payload: BountyCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    bounty = bounty_service.bounty_creation(payload, user, db, background_tasks)
    return BountyPublic.model_validate(bounty)


@router.post("/{bid}/submit", dependencies=[Depends(verify_frontend_key)])
@limiter.limit("100/minute")
def submit_bounty(
    request: Request,
    bid: int,
    body: BountySubmission,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    bounty = db.query(Bounty).filter(Bounty.id == bid).first()
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    created_time = datetime.now(timezone.utc)
    bounty_service.bounty_submission(body, user, bid, db, created_time, background_tasks)
    return {
        "Message": "Submission successful",
        "Bounty": bounty,
        "Submission": {
            "user_email": user.email,
            "proof": body.proof,
            "timestamp": created_time,
        },
    }
