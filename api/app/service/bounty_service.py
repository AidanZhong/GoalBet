# -*- coding: utf-8 -*-
"""
Created on 2025/10/14 20:39

@author: Aidan
@project: GoalBet
@filename: bounty_service
@description: 
- Python 
"""
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.app.core.events import broadcast
from api.app.models.bounty_missions import BountyCreate, BountySubmission
from api.app.models.db_models import User, Bounty, Submission


async def bounty_creation(payload: BountyCreate, user: User, db: Session):
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
    await broadcast("bounty.created", {
        "owner_email": user.email,
        "title": payload.title,
        "description": payload.description,
        "reward": payload.reward,
        "deadline": payload.deadline,
    })
    return bounty


def get_bounty(db: Session, bid: int):
    return db.query(Bounty).filter(Bounty.id == bid).first()


async def bounty_submission(payload: BountySubmission, user: User, bid: int, db: Session, created_time):
    bounty = get_bounty(db, bid)
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    # Convert `bounty.deadline` to a timezone-aware datetime, assuming it's UTC
    if bounty.deadline.tzinfo is None:
        bounty_deadline_aware = bounty.deadline.replace(tzinfo=timezone.utc)
    else:
        bounty_deadline_aware = bounty.deadline

    if bounty_deadline_aware < created_time:
        raise HTTPException(status_code=400, detail="Bounty has expired")

    submission = Submission(
        proof=payload.proof,
        bounty_id=bid,
        user_id=user.id,
        created_at=created_time
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    await broadcast("bounty.submission", {
        "bounty_id": bid,
        "user_email": user.email
    })
