# -*- coding: utf-8 -*-
"""
Created on 2025/10/5 10:05

@author: Aidan
@project: GoalBet
@filename: db_models
@description: 
- Python 
"""
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum, Float
from sqlalchemy.orm import relationship

from api.app.core.db import Base
from api.app.models.bet import BetSide, BetStatus
from api.app.models.enums import GoalStatus


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Integer, default=1000)
    goals = relationship("Goal", back_populates="owner")
    bets = relationship("Bet", back_populates="user")
    goal_updates = relationship("GoalUpdate", back_populates="author")
    bounties = relationship("Bounty", back_populates="owner")
    submissions = relationship("Submission", back_populates="user")


class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    deadline = Column(DateTime)
    status = Column(Enum(GoalStatus), default=GoalStatus.ACTIVE)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="goals")
    updates = relationship("GoalUpdate", back_populates="goal")
    bets = relationship("Bet", back_populates="goal")

    @property
    def owner_email(self):
        return self.owner.email if self.owner else None


class GoalUpdate(Base):
    __tablename__ = "goal_updates"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    goal_id = Column(Integer, ForeignKey("goals.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    goal = relationship("Goal", back_populates="updates")
    author = relationship("User", back_populates="goal_updates")

    @property
    def author_email(self):
        return self.author.email if self.author else None


class Bet(Base):
    __tablename__ = "bets"
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    side = Column(Enum(BetSide))
    amount = Column(Integer)
    odds_snapshot = Column(Float)
    status = Column(Enum(BetStatus), default=BetStatus.PENDING)
    payout = Column(Integer)
    goal = relationship("Goal", back_populates="bets")
    user = relationship("User", back_populates="bets")

    @property
    def user_email(self):
        return self.user.email if self.user else None


class Bounty(Base):
    __tablename__ = "bounties"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    reward = Column(Integer)
    deadline = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    submissions = relationship("Submission", back_populates="bounty")
    owner = relationship("User", back_populates="bounties")

    @property
    def owner_email(self):
        return self.owner.email if self.owner else None


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    proof = Column(Text)
    bounty_id = Column(Integer, ForeignKey("bounties.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    bounty = relationship("Bounty", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
