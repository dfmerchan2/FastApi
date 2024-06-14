import json
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from config.database import DBConnection
from core.models.user_model import User
from core.services.user_service import UserService
from test.conftest.mocks_services import user_info, user_update
from main import app

client = TestClient(app)


@pytest.fixture()
def mock_get_db():
    mock_db = DBConnection().connect_db()
    return mock_db


@pytest.mark.unit
@patch("core.services.user_service.UserService.create_user")
def test_service_add_user(mock_new_user, mock_get_db):
    user = user_info()
    user_db = User(**user)
    mock_new_user.return_value = user_db
    result = UserService(mock_get_db).create_user(user_db)
    assert result is not None
    assert result.id == 1023952
    assert result.email == "test@gmail.com"


@pytest.mark.unit
@patch("core.services.user_service.UserService.get_users")
def test_service_get_users(mock_get_users, mock_get_db):
    user = user_info()
    user_db = User(**user)
    mock_get_users.return_value = [user_db]
    result = UserService(mock_get_db).get_users()
    assert result is not None
    assert result[0].id == 1023952
    assert result[0].email == "test@gmail.com"


@pytest.mark.unit
@patch("core.services.user_service.UserService.get_user_by_id")
def test_service_get_user_by_id(mock_get_user, mock_get_db):
    user = user_info()
    user_db = User(**user)
    mock_get_user.return_value = user_db
    result = UserService(mock_get_db).get_user_by_id(user["id"])
    assert result is not None
    assert result.id == 1023952
    assert result.email == "test@gmail.com"


@pytest.mark.unit
@patch("core.services.user_service.UserService.update_user")
def test_service_update_user_by_id(mock_update_user, mock_get_db):
    user = user_info()
    user_data_update = user_update()
    user_db = User(**user)
    mock_update_user.return_value = user_data_update
    result = UserService(mock_get_db).update_user(user_db, user_data_update)
    assert result is not None
    assert result.name == user_data_update.name


@pytest.mark.unit
@patch("core.services.user_service.UserService.delete_user")
def test_service_delete_user_by_id(mock_delete_user, mock_get_db):
    user = user_info()
    user_db = User(**user)
    mock_delete_user.return_value = ''
    result = UserService(mock_get_db).delete_user(user_db)
    assert result == ''
