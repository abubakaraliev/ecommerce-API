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
    response = client.post('/user/signup', json=user_data)
    return response

def test_signup():
    sign_up_data = {
        "username": fake.name(),
        "email": fake.email(),
        "password": "password"
    }
    response = client.post('/user/signup', json=sign_up_data)
    assert response.status_code == 201
    assert response.json() == {
        "message": "signup successful"
    }
    
def test_login():
    response = get_user_data()
    login_data = {
        "username": "Richard Collins",
        "password": "password"
    }
    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200

    