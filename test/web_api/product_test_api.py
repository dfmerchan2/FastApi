from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from core.models.products_model import Product
from core.authenticator.role_checker import jwt
from main import app
from test.conftest.mocks_apis import get_jwt_manager, get_jwt_admin, product_req_api, product_update_req_api
from test.conftest.mocks_services import product_info

client = TestClient(app)


@pytest.mark.api
@patch("core.services.product_service.ProductService.get_product")
def test_get_products_api(mock_get_product):
    app.dependency_overrides[jwt] = get_jwt_manager
    product_mock = product_info()
    mock_get_product.return_value = [Product(**product_mock)]
    resp = client.get(url=f'/products', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json()[0] == product_mock


@pytest.mark.api
def test_get_products_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    resp = client.get(url=f'/products', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.product_service.ProductService.get_product_by_name")
def test_get_product_by_name_api(mock_get_product):
    app.dependency_overrides[jwt] = get_jwt_manager
    product_mock = product_info()
    mock_get_product.return_value = Product(**product_mock)
    resp = client.get(url=f'/product?product_name=Test', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json() == product_mock


@pytest.mark.api
@patch("core.services.product_service.ProductService.get_product_by_name")
def test_get_product_by_name_api_product_not_found(mock_product):
    app.dependency_overrides[jwt] = get_jwt_manager
    mock_product.return_value = ""
    resp = client.get(url=f'/product?product_name=Test', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 404
    assert resp.json() == 'Product not found'


@pytest.mark.api
def test_get_product_by_name_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    resp = client.get(url=f'/product?product_name=Test', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.product_service.ProductService.create_product")
def test_create_product_api(mock_get_product):
    app.dependency_overrides[jwt] = get_jwt_manager
    product_req = product_req_api()
    product_mock = product_info()
    mock_get_product.return_value = Product(**product_mock)
    resp = client.post(url=f'/product/create', headers={"Authorization": f"Bearer TestAuto"}, content=product_req)
    assert resp.status_code == 201
    assert resp.json() == "Product register successfully"


@pytest.mark.api
def test_create_product_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    product_req = product_req_api()
    resp = client.post(url=f'/product/create', headers={"Authorization": f"Bearer TestAuto"}, content=product_req)
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.product_service.ProductService.get_product_by_id")
@patch("core.services.product_service.ProductService.update_product")
def test_update_product_api(mock_get_product, mock_update_prod):
    app.dependency_overrides[jwt] = get_jwt_manager
    product_req = product_update_req_api()
    product_mock = product_info()
    mock_get_product.return_value = Product(**product_mock)
    mock_update_prod.return_value = Product(**product_mock)
    resp = client.put(url=f'/product/update?product_id=12345', headers={"Authorization": f"Bearer TestAuto"}, content=product_req)
    assert resp.status_code == 200
    assert resp.json() == product_mock


@pytest.mark.api
@patch("core.services.product_service.ProductService.get_product_by_id")
def test_update_product_api_product_not_found(mock_product):
    app.dependency_overrides[jwt] = get_jwt_manager
    product_req = product_update_req_api()
    mock_product.return_value = ""
    resp = client.put(url=f'/product/update?product_id=12345', headers={"Authorization": f"Bearer TestAuto"}, content=product_req)
    assert resp.status_code == 404
    assert resp.json() == 'Product not found'


@pytest.mark.api
def test_update_product_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    product_req = product_update_req_api()
    resp = client.put(url=f'/product/update?product_id=12345', headers={"Authorization": f"Bearer TestAuto"},
                      content=product_req)
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.product_service.ProductService.get_product_by_id")
@patch("core.services.product_service.ProductService.delete_product")
def test_delete_product_api(mock_delete_product, mock_get_prod):
    app.dependency_overrides[jwt] = get_jwt_manager
    product_mock = product_info()
    mock_get_prod.return_value = Product(**product_mock)
    mock_delete_product.return_value = ""
    resp = client.delete(url=f'/product/delete?product_id=12345', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json() == "Product was deleted"


@pytest.mark.api
@patch("core.services.product_service.ProductService.get_product_by_id")
def test_delete_product_api_product_not_found(mock_product):
    app.dependency_overrides[jwt] = get_jwt_manager
    mock_product.return_value = ""
    resp = client.delete(url=f'/product/delete?product_id=12345', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 404
    assert resp.json() == 'Product not found'


@pytest.mark.api
def test_update_product_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    resp = client.delete(url=f'/product/delete?product_id=12345', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""

