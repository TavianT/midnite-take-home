from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime

import sys
sys.path.insert(0, "../src")
from main import app, get_db
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_non_alert_request():
    response = client.post(
        "/event",
        json={
            "type": "deposit", 
            "amount": "42.00", 
            "user_id": 1, 
            "time": 1
        })
    assert response.status_code == 200
    data = response.json()
    assert data["alert"] == False
    assert data["alert_codes"] == []
    assert data["user_id"] == 1

def test_code_1100():
    response = client.post(
        "/event",
        json={
            "type": "withdrawal", 
            "amount": "142.00", 
            "user_id": 1, 
            "time": 2
        })
    assert response.status_code == 200
    data = response.json()
    assert data["alert"] == True
    assert data["alert_codes"] == [1100]
    assert data["user_id"] == 1

def test_code_30():
    response = client.post(
        "/event",
        json={
            "type": "withdrawal", 
            "amount": "14.00", 
            "user_id": 1, 
            "time": 3
        })
    assert response.status_code == 200
    response = client.post(
        "/event",
        json={
            "type": "withdrawal", 
            "amount": "14.00", 
            "user_id": 1, 
            "time": 4
        })
    assert response.status_code == 200
    response = client.post(
        "/event",
        json={
            "type": "withdrawal", 
            "amount": "14.00", 
            "user_id": 1, 
            "time": 5
        })
    assert response.status_code == 200
    data = response.json()
    assert data["alert"] == True
    assert data["alert_codes"] == [30]
    assert data["user_id"] == 1

def test_code_300():
    response = client.post(
        "/event",
        json={
            "type": "deposit", 
            "amount": "14.00", 
            "user_id": 1, 
            "time": 6
        })
    assert response.status_code == 200
    response = client.post(
        "/event",
        json={
            "type": "deposit", 
            "amount": "15.00", 
            "user_id": 1, 
            "time": 7
        })
    assert response.status_code == 200
    response = client.post(
        "/event",
        json={
            "type": "deposit", 
            "amount": "16.00", 
            "user_id": 1, 
            "time": 8
        })
    assert response.status_code == 200
    data = response.json()
    assert data["alert"] == True
    assert data["alert_codes"] == [300]
    assert data["user_id"] == 1

def test_code_123():
    response = client.post(
        "/event",
        json={
            "type": "deposit", 
            "amount": "114.00", 
            "user_id": 1, 
            "time": 31
        })
    assert response.status_code == 200
    print(response.text)
    response = client.post(
        "/event",
        json={
            "type": "deposit", 
            "amount": "5.00", 
            "user_id": 1, 
            "time": 37
        })
    assert response.status_code == 200
    print(response.text)
    response = client.post(
        "/event",
        json={
            "type": "deposit", 
            "amount": "166.00", 
            "user_id": 1, 
            "time": 45
        })
    assert response.status_code == 200
    print(response.text)
    data = response.json()
    assert data["alert"] == True
    assert data["alert_codes"] == [123]
    assert data["user_id"] == 1
