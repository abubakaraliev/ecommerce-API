from core.user.models import User


def test_create_user():
    user = User(
        id=1,
        username="test",
        email="test@example.com",
        password="password")
    assert user.id == 1
    assert user.username == "test"
    assert user.email == "test@example.com"
    assert user.password == "password"