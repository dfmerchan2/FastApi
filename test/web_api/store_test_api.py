from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from core.models.product_store_model import ProductStore
from core.models.products_model import Product
from core.authenticator.role_checker import jwt
from main import app
from test.conftest.mocks_apis import get_jwt_admin, get_jwt_manager, store_req_api, store_update_req_api
from test.conftest.mocks_services import product_store_info, product_info

client = TestClient(app)


@pytest.mark.api
@patch("core.services.product_store_service.ProductStoreService.get_products_store")
def test_get_stores_api(mock_get_store):
    app.dependency_overrides[jwt] = get_jwt_manager
    store_mock = product_store_info()
    mock_get_store.return_value = [ProductStore(**store_mock)]
    resp = client.get(url=f'/product/store', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json()[0] == store_mock


@pytest.mark.api
def test_get_stores_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    resp = client.get(url=f'/product/store', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.product_store_service.ProductStoreService.get_product_store_by_id")
def test_get_store_by_id_api(mock_get_store):
    app.dependency_overrides[jwt] = get_jwt_manager
    store_mock = product_store_info()
    mock_get_store.return_value = ProductStore(**store_mock)
    resp = client.get(url=f'/product/store/?product_store_id=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json() == store_mock


@pytest.mark.api
@patch("core.services.product_store_service.ProductStoreService.get_product_store_by_id")
def test_get_store_by_id_api_product_not_found(mock_store):
    app.dependency_overrides[jwt] = get_jwt_manager
    mock_store.return_value = ""
    resp = client.get(url=f'/product/store/?product_store_id=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 404
    assert resp.json() == 'Product store not found'


@pytest.mark.api
def test_get_store_by_id_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    resp = client.get(url=f'/product/store/?product_store_id=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.product_service.ProductService.get_product_by_name")
@patch("core.services.product_store_service.ProductStoreService.create_product_store")
def test_create_store_api(mock_get_store, mock_create_store):
    app.dependency_overrides[jwt] = get_jwt_manager
    store_req = store_req_api()
    store_mock = product_store_info()
    product_mock = product_info()
    mock_get_store.return_value = Product(**product_mock)
    mock_create_store.return_value = ProductStore(**store_mock)
    resp = client.post(url=f'/store/create?product_name=test', headers={"Authorization": f"Bearer TestAuto"}, content=store_req)
    assert resp.status_code == 201
    assert resp.json() == "Product Store register successfully"


@pytest.mark.api
def test_create_store_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    store_req = store_req_api()
    resp = client.post(url=f'/store/create?product_name=test', headers={"Authorization": f"Bearer TestAuto"}, content=store_req)
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.product_store_service.ProductStoreService.get_product_store_by_id")
@patch("core.services.product_store_service.ProductStoreService.update_product_store")
def test_update_store_api(mock_get_store, mock_update_store):
    app.dependency_overrides[jwt] = get_jwt_manager
    store_req = store_update_req_api()
    store_mock = product_store_info()
    mock_get_store.return_value = ProductStore(**store_mock)
    mock_update_store.return_value = ProductStore(**store_mock)
    resp = client.put(url=f'/store/update?product_store_id=1', headers={"Authorization": f"Bearer TestAuto"}, content=store_req)
    assert resp.status_code == 200
    assert resp.json() == store_mock


@pytest.mark.api
@patch("core.services.product_store_service.ProductStoreService.get_product_store_by_id")
def test_update_store_api_product_not_found(mock_store):
    app.dependency_overrides[jwt] = get_jwt_manager
    store_req = store_update_req_api()
    mock_store.return_value = ""
    resp = client.put(url=f'/store/update?product_store_id=1', headers={"Authorization": f"Bearer TestAuto"}, content=store_req)
    assert resp.status_code == 404
    assert resp.json() == 'Store not found'


@pytest.mark.api
def test_update_store_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    store_req = store_update_req_api()
    resp = client.put(url=f'/store/update?product_store_id=1', headers={"Authorization": f"Bearer TestAuto"},
                      content=store_req)
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.product_store_service.ProductStoreService.get_product_store_by_id")
@patch("core.services.product_store_service.ProductStoreService.delete_product_store")
def test_delete_product_api(mock_delete_store, mock_get_store):
    app.dependency_overrides[jwt] = get_jwt_manager
    store_mock = product_store_info()
    mock_get_store.return_value = ProductStore(**store_mock)
    mock_delete_store.return_value = ""
    resp = client.delete(url=f'/store/delete?product_store_id=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json() == "Store was deleted"


@pytest.mark.api
@patch("core.services.product_store_service.ProductStoreService.get_product_store_by_id")
def test_delete_product_api_product_not_found(mock_store):
    app.dependency_overrides[jwt] = get_jwt_manager
    mock_store.return_value = ""
    resp = client.delete(url=f'/store/delete?product_store_id=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 404
    assert resp.json() == 'Store not found'


@pytest.mark.api
def test_update_product_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    resp = client.delete(url=f'/store/delete?product_store_id=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""

