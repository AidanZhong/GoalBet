import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.app.core.db import Base, get_db
from api.app.main import app

# Shared in-memory DB for all connections
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # ← keeps one shared memory DB
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables once
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# Override get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Provide test client
@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    print("🧹 Resetting DB before test...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def captured_email(monkeypatch):
    sent = {"to": None, "subject": None, "body": None}

    def fake_send_email(*, to, subject, body):
        sent["to"] = to
        sent["subject"] = subject
        sent["body"] = body

    monkeypatch.setattr("api.app.service.tokens_helper.send_email", fake_send_email, raising=False)
    return sent
