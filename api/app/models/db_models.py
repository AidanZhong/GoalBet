# -*- coding: utf-8 -*-
"""
Created on 2025/10/5 10:05

@author: Aidan
@project: GoalBet
@filename: db_models
"""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
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

    email_verified_at = Column(DateTime, nullable=True)
    username = Column(String(20))
    avatar_url = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=func.now())

    goals = relationship("Goal", back_populates="owner", cascade="all, delete-orphan")
    bets = relationship("Bet", back_populates="user", cascade="all, delete-orphan")
    goal_updates = relationship("GoalUpdate", back_populates="author", cascade="all, delete-orphan")
    bounties = relationship("Bounty", back_populates="owner", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    tokens = relationship("UserToken", back_populates="user", cascade="all, delete-orphan")


# used for email verification
class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(128), unique=True, nullable=False)
    kind = Column(String(16), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    consumed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="tokens")


class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    deadline = Column(DateTime)
    status = Column(Enum(GoalStatus), default=GoalStatus.ACTIVE)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="goals")
    updates = relationship("GoalUpdate", back_populates="goal", cascade="all, delete-orphan")
    bets = relationship("Bet", back_populates="goal", cascade="all, delete-orphan")

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
    submissions = relationship("Submission", back_populates="bounty", cascade="all, delete-orphan")
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
