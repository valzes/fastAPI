
from app.models import schemas
import pytest


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Welcome to Fast API!!"
    assert res.status_code == 200


def test_user_create(client):
    res = client.post(
        "/users/", json={"email": "val4@val.com", "password": "val"})
    new_user = schemas.ResponseUser(**res.json())
    assert new_user.email == "val4@val.com"
    assert res.status_code == 201


@pytest.mark.parametrize("email, password, create_user", [("abc@abc.com", "abc", ("abc@abc.com", "abc"))], indirect=["create_user"])
def test_login_user(client, email, password, create_user):
    res = client.post(
        "/login", data={"username": email, "password": password})
    assert res.status_code == 200
    assert res.json().get("token_type") == "bearer"


@pytest.mark.parametrize("email, password, sts_code, detail, create_user", [("abc@abc.com", "abc1", 401, "Incorrect password", ("abc@abc.com", "abc")),
                                                                            ("abc1@abc.com", "abc", 404, "User not found", ("abc@abc.com", "abc"))], indirect=["create_user"])
def test_login_user_incorrect_password(client, email, password, sts_code, detail, create_user):
    res = client.post(
        "/login", data={"username": email, "password": password})
    assert res.status_code == sts_code
    assert res.json().get("detail") == detail
