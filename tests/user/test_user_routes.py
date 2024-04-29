from fastapi.testclient import TestClient
from app import app
from faker import Faker

fake = Faker()
client = TestClient(app)

def get_user_data():
    user_data = {
        "username": fake.name(),
        "email": fake.email(),
        "password": "password"
    }
    response = client.post('/api/signup', json=user_data)
    return response

def test_signup():
    sign_up_data = {
        "username": fake.name(),
        "email": fake.email(),
        "password": "password"
    }
    response = client.post('/api/signup', json=sign_up_data)
    assert response.status_code == 201
    assert response.json() == {
        "message": "signup successful"
    }
    
def test_login():
    response = get_user_data()
    login_data = {
        "username": "Daniel Burns",
        "password": "password"
    }
    response = client.post('/api/login', json=login_data)
    assert response.status_code == 200
    
def test_update_user():
    update_user = {
       "username": "Updated Daniel Burns",
       "email": "Daniel@updated.com",
       "password": "password"
       
    }
    response = client.put(f"/api/users/<int:id>?id=75", json=update_user)
    assert response.status_code == 200

    