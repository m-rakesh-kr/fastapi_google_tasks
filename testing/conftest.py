import os
import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture
def token_header(client: TestClient):
    data = {
        "name": 'TestUser',
        "email": 'testing@gmail.com',
        "password": '@test9097RK',
        "confirm_password": '@test9097RK'
    }
    response = client.post('/api/v1/auth/register', json.dumps(data))
    data = {
        "username": "testing@gmail.com",
        "password": "@test9097RK"
    }
    response = client.post("/api/v1/auth/login", data)
    # print(f"RESPONSE {response.json()}")
    access_token = response.json()["access_token"]
    # print(access_token)
    return f"Bearer {access_token}"


@pytest.fixture
def reset_password_access_token(client: TestClient):
    data = {
        "email": os.getenv('email'),
    }
    response = client.post('/api/v1/auth/forgot_password', json.dumps(data))
    # print(f"RESPONSE {response.json()}")
    access_token = response.json()['Reset Password Link'].split('/')[-1]
    return access_token



