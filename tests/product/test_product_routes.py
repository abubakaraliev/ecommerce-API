from fastapi.testclient import TestClient
from app import app
import random
from faker import Faker

fake = Faker()
client = TestClient(app)
def get_product_data():
    product_data = {
        "identifier": fake.name(),
        "price": random.randint(1, 1000),
        "is_available": True | False
    }
    response = client.post('/user/products', json=product_data)
    return response
    
    
def test_createproduct():
    product_create_data = {
        "identifier": fake.name(),
        "price": str(random.randint(1, 1000)),
        "is_available": True | False
    }
    response = client.post('/user/products', json=product_create_data)
    assert response.status_code == 201
    assert response.json() == {
        "message": "product created successfully"
    }