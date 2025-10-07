import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from api.app.core.db import Base, get_db
from api.app.main import app

# 1️⃣  Shared in-memory DB for all connections
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # ← keeps one shared memory DB
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2️⃣  Create all tables once
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# 3️⃣  Override get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# 4️⃣  Provide test client
@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    print("🧹 Resetting DB before test...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
