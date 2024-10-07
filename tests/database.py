from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from alembic.config import Config
from alembic import command

# Database URL for the test environment
SQLACHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# Create a new engine for the test database
engine = create_engine(SQLACHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Path to Alembic's configuration file
alembic_cfg = Config("alembic.ini")

@pytest.fixture()
def session():
    # Drop all tables before each test
    Base.metadata.drop_all(bind=engine)

    # Apply migrations using Alembic
    command.upgrade(alembic_cfg, "head")

    # Create a new session for the test database
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    # Override the dependency with the test session
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
