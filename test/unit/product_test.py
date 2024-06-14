from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from config.database import DBConnection
from core.models.products_model import Product
from core.services.product_service import ProductService
from main import app
from test.conftest.mocks_services import product_info, product_update

client = TestClient(app)


@pytest.fixture()
def mock_get_db():
    mock_db = DBConnection().connect_db()
    return mock_db


@pytest.mark.unit
@patch("core.services.product_service.ProductService.create_product")
def test_service_create_product(mock_new_product, mock_get_db):
    product = product_info()
    product_db = Product(**product)
    mock_new_product.return_value = product_db
    result = ProductService(mock_get_db).create_product(product_db)
    assert result is not None
    assert result.name == product["name"]


@pytest.mark.unit
@patch("core.services.product_service.ProductService.get_product")
def test_service_get_products(mock_get_products, mock_get_db):
    product = product_info()
    product_db = Product(**product)
    mock_get_products.return_value = [product_db]
    result = ProductService(mock_get_db).get_product()
    assert result is not None
    assert result[0].name == product["name"]


@pytest.mark.unit
@patch("core.services.product_service.ProductService.get_product_by_id")
def test_service_get_product_by_id(mock_get_product_id, mock_get_db):
    product = product_info()
    product_db = Product(**product)
    mock_get_product_id.return_value = product_db
    result = ProductService(mock_get_db).get_product_by_id("1")
    assert result is not None
    assert result.name == product["name"]


@pytest.mark.unit
@patch("core.services.product_service.ProductService.get_product_by_name")
def test_service_get_product_by_name(mock_get_product_name, mock_get_db):
    product = product_info()
    product_db = Product(**product)
    mock_get_product_name.return_value = product_db
    result = ProductService(mock_get_db).get_product_by_name(product["name"])
    assert result is not None
    assert result.name == product["name"]


@pytest.mark.unit
@patch("core.services.product_service.ProductService.update_product")
def test_service_update_product(mock_update_product, mock_get_db):
    product = product_info()
    product_up = product_update()
    product_db = Product(**product)
    mock_update_product.return_value = product_up
    result = ProductService(mock_get_db).update_product(product_db, product_up)
    assert result is not None
    assert result.name == product_up.name


@pytest.mark.unit
@patch("core.services.product_service.ProductService.delete_product")
def test_service_delete_product(mock_delete_product, mock_get_db):
    product = product_info()
    product_db = Product(**product)
    mock_delete_product.return_value = ""
    result = ProductService(mock_get_db).delete_product(product_db)
    assert result == ""
