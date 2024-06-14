import json

import pytest
from fastapi.testclient import TestClient

from core.authenticator.jwt_manager import create_token, validate_token
from core.schema.user_dto import LoginDTO
from main import app


client = TestClient(app)


@pytest.mark.unit
def test_create_token():
    data: dict = {"login": "test@gmail.com", "password": "123456", "role": "Admin"}
    token = create_token(data)
    assert token is not ''


@pytest.mark.unit
def test_validate_token():
    data: dict = {"login": "test@gmail.com", "password": "123456", "role": "Admin"}
    token = create_token(data)
    validate = validate_token(token)
    assert validate["login"] == "test@gmail.com"
    assert validate["password"] == "123456"
    assert validate["role"] == "Admin"


@pytest.mark.unit
def test_login_success():
    role = "Admin"
    user_login: LoginDTO = LoginDTO(login="test@gmail.com", password="12345")
    user_dict = user_login.model_dump()
    json_str = json.dumps(user_dict)
    resp = client.post(url=f'/login?role={role}', content=json_str)
    assert resp.status_code == 200
    assert resp.json() is not None



