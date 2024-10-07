from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

# Database URL for the test environment
SQLACHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# Create a new engine and session for the test database
engine = create_engine(SQLACHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    # Drop all tables before each test to ensure a clean state
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Create a new session for each test
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

@pytest.fixture
def test_user(client):
    user_data = {"email": "bafana@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "bafana123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    # Generate access token for the test_user
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    # Use a copy of the client headers to avoid side effects
    headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    client.headers = headers
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = [
        {"title": "first title", "content": "first content", "owner_id": test_user['id']},
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user['id']},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user['id']},
        {"title": "4th title", "content": "4th content", "owner_id": test_user2['id']}  # Fixed title repetition  
    ]

    # Map post data to Post models
    posts = [models.Post(**post) for post in post_data]
    
    # Add and commit posts to the session
    session.add_all(posts)
    session.commit()

    # Return all posts
    return session.query(models.Post).all()
