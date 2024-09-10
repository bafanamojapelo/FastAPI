import pytest
from app import schemas
from .database import client, session
    

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200

def test_create_and_login_user(client):
    # Create a new user first
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    assert res.status_code == 201

    # Now attempt to log in
    res = client.post("/login", data={"username": "hello123@gmail.com", "password": "password123"})
    print(res.json())  # To inspect if there's any issue
    assert res.status_code == 200



