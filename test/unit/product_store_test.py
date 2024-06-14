from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from config.database import DBConnection
from core.models.product_store_model import ProductStore
from core.services.product_store_service import ProductStoreService
from main import app
from test.conftest.mocks_services import product_store_info, product_store_update

client = TestClient(app)


@pytest.fixture()
def mock_get_db():
    mock_db = DBConnection().connect_db()
    return mock_db


@pytest.mark.unit
@patch("core.services.product_store_service.ProductStoreService.create_product_store")
def test_service_create_store(mock_new_product_store, mock_get_db):
    product_store = product_store_info()
    store_db = ProductStore(**product_store)
    mock_new_product_store.return_value = store_db
    result = ProductStoreService(mock_get_db).create_product_store(store_db)
    assert result is not None
    assert result.availability_qty == product_store["availability_qty"]


@pytest.mark.unit
@patch("core.services.product_store_service.ProductStoreService.get_products_store")
def test_service_get_stores(mock_get_product_stores, mock_get_db):
    product_store = product_store_info()
    store_db = ProductStore(**product_store)
    mock_get_product_stores.return_value = [store_db]
    result = ProductStoreService(mock_get_db).get_products_store()
    assert result is not None
    assert result[0].availability_qty == product_store["availability_qty"]


@pytest.mark.unit
@patch("core.services.product_store_service.ProductStoreService.get_product_store_by_id")
def test_service_get_store_by_id(mock_get_store_by_id, mock_get_db):
    product_store = product_store_info()
    store_db = ProductStore(**product_store)
    mock_get_store_by_id.return_value = store_db
    result = ProductStoreService(mock_get_db).get_product_store_by_id(1)
    assert result is not None
    assert result.availability_qty == product_store["availability_qty"]


@pytest.mark.unit
@patch("core.services.product_store_service.ProductStoreService.update_product_store")
def test_service_update_store(mock_update_store, mock_get_db):
    product_store = product_store_info()
    store_update = product_store_update()
    store_db = ProductStore(**product_store)
    mock_update_store.return_value = store_update
    result = ProductStoreService(mock_get_db).update_product_store(store_db, store_update)
    assert result is not None
    assert result.availability_qty == store_update.availability_qty


@pytest.mark.unit
@patch("core.services.product_store_service.ProductStoreService.delete_product_store")
def test_service_delete_store(mock_delete_store, mock_get_db):
    product_store = product_store_info()
    store_db = ProductStore(**product_store)
    mock_delete_store.return_value = ""
    result = ProductStoreService(mock_get_db).delete_product_store(store_db)
    assert result == ""

