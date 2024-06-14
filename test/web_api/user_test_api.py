from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from config.database import DBConnection
from core.models.role_model import Role
from core.models.user_model import User
from core.authenticator.role_checker import jwt
from main import app
from test.conftest.mocks_apis import get_jwt_admin, get_jwt_customer, get_jwt_manager, role_info, user_req_api, \
    user_update_req_api
from test.conftest.mocks_services import user_info


client = TestClient(app)


@pytest.mark.api
@patch("core.services.user_service.UserService.get_users")
def test_get_users_api(mock_get_users):
    app.dependency_overrides[jwt] = get_jwt_admin
    user_mock = user_info()
    mock_get_users.return_value = [User(**user_mock)]
    resp = client.get(url=f'/users', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json()[0] == user_mock


@pytest.mark.api
def test_get_users_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_customer
    resp = client.get(url=f'/users', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.user_service.UserService.get_user_by_id")
def test_get_user_by_id_api(mock_get_user):
    app.dependency_overrides[jwt] = get_jwt_admin
    user_mock = user_info()
    user_id = user_mock["id"]
    mock_get_user.return_value = User(**user_mock)
    resp = client.get(url=f'/user/id/?id_user={user_id}', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json() == user_mock


@pytest.mark.api
def test_get_user_by_id_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_manager
    user_mock = user_info()
    user_id = user_mock["id"]
    resp = client.get(url=f'/user/id/?id_user={user_id}', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.user_service.UserService.get_user_by_id")
def test_get_user_by_id_api_id_not_found(mock_get_user):
    app.dependency_overrides[jwt] = get_jwt_customer
    user_mock = user_info()
    user_id = user_mock["id"]
    mock_get_user.return_value = ""
    resp = client.get(url=f'/user/id/?id_user={user_id}', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 404
    assert resp.json() == "Id not found"


@pytest.mark.api
@patch("core.services.role_service.RoleService.get_role_by_name")
@patch("core.services.user_service.UserService.create_user")
def test_create_new_user_api(mock_get_rol, mock_create_user):
    user_req = user_req_api()
    usr_mock_db = user_info()
    role_mock_db = role_info()
    mock_get_rol.return_value = Role(**role_mock_db)
    mock_create_user.return_value = User(**usr_mock_db)
    resp = client.post(url=f'/user/create?role=Admin', headers={"Authorization": f"Bearer TestAuto"}, content=user_req)
    assert resp.status_code == 201
    assert resp.json() == "User register successfully"


@pytest.mark.api
@patch("core.services.user_service.UserService.get_user_by_id")
@patch("core.services.user_service.UserService.update_user")
def test_update_user(mock_update_user, mock_get_user):
    app.dependency_overrides[jwt] = get_jwt_customer
    user_req = user_update_req_api()
    user_mock = user_info()
    user_id = user_mock["id"]
    mock_get_user.return_value = User(**user_mock)
    mock_update_user.return_value = User(**user_mock)
    resp = client.put(url=f'/user/update?id_user={user_id}', headers={"Authorization": f"Bearer TestAuto"}, content=user_req)
    assert resp.status_code == 200
    assert resp.json() == user_mock


@pytest.mark.api
@patch("core.services.user_service.UserService.get_user_by_id")
def test_update_user_id_not_found(mock_get_user):
    app.dependency_overrides[jwt] = get_jwt_customer
    user_req = user_update_req_api()
    user_mock = user_info()
    user_id = user_mock["id"]
    mock_get_user.return_value = ""
    resp = client.put(url=f'/user/update?id_user={user_id}', headers={"Authorization": f"Bearer TestAuto"}, content=user_req)
    assert resp.status_code == 404
    assert resp.json() == "Id not found"


@pytest.mark.api
def test_update_user_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_manager
    user_req = user_update_req_api()
    user_mock = user_info()
    user_id = user_mock["id"]
    resp = client.put(url=f'/user/update?id_user={user_id}', headers={"Authorization": f"Bearer TestAuto"}, content=user_req)
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.user_service.UserService.get_user_by_id")
@patch("core.services.user_service.UserService.delete_user")
def test_delete_user(mock_delete_user, mock_get_user):
    app.dependency_overrides[jwt] = get_jwt_customer
    user_mock = user_info()
    user_id = user_mock["id"]
    mock_get_user.return_value = User(**user_mock)
    mock_delete_user.return_value = ""
    resp = client.delete(url=f'/user/delete?id_user={user_id}', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json() == 'User was deleted'


@pytest.mark.api
@patch("core.services.user_service.UserService.get_user_by_id")
def test_delete_user_id_not_found(mock_get_user):
    app.dependency_overrides[jwt] = get_jwt_customer
    user_mock = user_info()
    user_id = user_mock["id"]
    mock_get_user.return_value=""
    resp = client.delete(url=f'/user/delete?id_user={user_id}', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 404
    assert resp.json() == "Id not found"


@pytest.mark.api
def test_delete_user_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_manager
    user_mock = user_info()
    user_id = user_mock["id"]
    resp = client.delete(url=f'/user/delete?id_user={user_id}', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""
