# -*- coding: utf-8 -*-
"""
Created on 2025/10/14 17:22

@author: Aidan
@project: GoalBet
@filename: goal_services
"""
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.app.core.events import broadcast
from api.app.models.bet import BetSide
from api.app.models.db_models import Bet, Goal, GoalUpdate, User
from api.app.models.enums import GoalStatus
from api.app.models.goal import GoalCreate, GoalPublic, GoalUpdateCreate


def create_goal(payload: GoalCreate, user: User, db: Session, background_tasks):
    # 统一将 deadline 归一化为 UTC aware datetime
    deadline = payload.deadline
    if deadline.tzinfo is None:
        # 视为 UTC
        deadline = deadline.replace(tzinfo=timezone.utc)
    else:
        # 转换为 UTC
        deadline = deadline.astimezone(timezone.utc)

    if deadline <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Goal deadline must be in the future")

    goal = Goal(
        title=payload.title,
        description=payload.description,
        deadline=payload.deadline,
        status=GoalStatus.ACTIVE,
        owner_id=user.id,
    )

    db.add(goal)
    db.commit()
    db.refresh(goal)

    background_tasks.add_task(broadcast, "goal.created", {"id": goal.id, "title": goal.title})
    return goal


def get_all_goals(db: Session):
    return [fill_the_market(g) for g in db.query(Goal).all()]


def get_goal(goal_id: int, db: Session):
    return fill_the_market(db.query(Goal).filter(Goal.id == goal_id).first())


def update_goal(goal_id: int, payload: GoalUpdateCreate, user: User, db: Session, background_tasks):
    goal = get_goal(goal_id, db)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    if goal.owner_email != user.email:
        raise HTTPException(status_code=403, detail="Only owner can post updates")

    update = GoalUpdate(
        goal_id=goal_id,
        content=payload.content,
        author_id=user.id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(update)
    db.commit()
    db.refresh(update)

    background_tasks.add_task(
        broadcast,
        "goal.update",
        {
            "goal updated": goal_id,
            "update id": update.id,
        },
    )
    return update


def get_goal_trends(db: Session):
    # ranked by price pool
    # Compute total pool for each goal
    pool_subquery = (
        db.query(Bet.goal_id, func.coalesce(func.sum(Bet.amount), 0).label("total_pool"))
        .group_by(Bet.goal_id)
        .subquery()
    )
    # join goals with their pools
    query = (
        db.query(Goal)
        .outerjoin(pool_subquery, Goal.id == pool_subquery.c.goal_id)
        .order_by(pool_subquery.c.total_pool.desc().nullslast())
    )
    goals = query.all()
    return goals


def list_user_goals(user: User, db: Session):
    return [fill_the_market(g) for g in db.query(Goal).filter(Goal.owner_id == user.id).all()]


def fill_the_market(g):
    supports = sum(b.amount for b in getattr(g, "bets", []) if b.side == BetSide.SUCCESS)
    againsts = sum(b.amount for b in getattr(g, "bets", []) if b.side == BetSide.FAIL)

    gp = GoalPublic.model_validate(g)
    gp.markets = [int(supports or 0), int(againsts or 0)]
    return gp
