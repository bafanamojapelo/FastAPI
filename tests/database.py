import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
from fastapi.testclient import TestClient  # Import TestClient
from app.main import app
from app.config import settings
from app.database import get_db, Base
from alembic import command

# Encode the password if it contains special characters
encoded_password = quote_plus(settings.database_password)


# Construct the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.database_username}:{encoded_password}@'
    f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
)

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





# Fixture to clear the database between tests
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_database():
    # Drop all tables before test
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables before test
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Optionally, drop all tables after test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")

def client(session):
    def override_get_db():
    
     try:
          yield session
     finally:
          session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)