from fastapi.testclient import TestClient
import pytest
from app import app

client = TestClient(app)


def test_create_user():
    try:
        response = client.post(
            "/createUser", json={"username": "test_user", "email": "test@example.com", "password": "test_password"})
        assert response.status_code == 201
    except Exception as e:
        pytest.fail(f"Failed with exception: {e}")

    try:
        response = client.post(
            "/createUser", json={"username": "test_user", "email": "test@example.com", "password": "test_password"})
        assert response.status_code == 400
    except Exception as e:
        pytest.fail(f"Failed with exception: {e}")


def test_get_product():
    try:
        response = client.get("products/<int:id>?id=6")
        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Failed with exception: {e}")

    try:
        response = client.get("products/<int:id>?id=9")
        assert response.status_code == 404
    except Exception as e:
        pytest.fail(f"Failed with exception: {e}")


def test_delete_all_users():
    try:
        response = client.delete("users/all")
        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Failed with exception: {e}")

    try:
        response = client.delete("users/all")
        assert response.status_code == 404
    except Exception as e:
        pytest.fail(f"Failed with exception: {e}")


def test_delete_all_products():
    try:
        response = client.delete("products/all")
        assert response.status_code == 200
    except Exception as e:
        pytest.fail(f"Failed with exception: {e}")

    try:
        response = client.delete("products/all")
        assert response.status_code == 404
    except Exception as e:
        pytest.fail(f"Failed with exception: {e}")
