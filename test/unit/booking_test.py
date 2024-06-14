from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from config.database import DBConnection
from core.models.booking_model import Booking
from core.models.products_model import Product
from core.models.status_model import Status
from core.models.user_model import User
from core.services.booking_service import BookingService
from main import app
from test.conftest.mocks_services import booking_info, user_info, product_info, status_info, booking_update

client = TestClient(app)


@pytest.fixture()
def mock_get_db():
    mock_db = DBConnection().connect_db()
    return mock_db


@pytest.mark.unit
@patch("core.services.booking_service.BookingService.create_booking")
def test_service_create_booking(mock_new_booking, mock_get_db):
    booking = booking_info()
    booking_db = Booking(**booking)
    mock_new_booking.return_value = booking_db
    result = BookingService(mock_get_db).create_booking(booking_db)
    assert result is not None
    assert result.delivery_address == booking["delivery_address"]


@pytest.mark.unit
@patch("core.services.booking_service.BookingService.get_booking")
def test_service_get_bookings(mock_get_bookings, mock_get_db):
    booking = booking_info()
    booking_db = Booking(**booking)
    mock_get_bookings.return_value = [booking_db]
    result = BookingService(mock_get_db).get_booking()
    assert result is not None
    assert result[0].delivery_address == booking["delivery_address"]


@pytest.mark.unit
@patch("core.services.booking_service.BookingService.get_booking_by_id")
def test_service_get_booking_id(mock_get_booking_id, mock_get_db):
    booking = booking_info()
    booking_db = Booking(**booking)
    mock_get_booking_id.return_value = booking_db
    result = BookingService(mock_get_db).get_booking_by_id(1)
    assert result is not None
    assert result.delivery_address == booking["delivery_address"]


@pytest.mark.unit
@patch("core.services.booking_service.BookingService.get_booking_by_user")
def test_service_get_booking_user(mock_get_booking_user, mock_get_db):
    booking = booking_info()
    booking_db = Booking(**booking)
    mock_get_booking_user.return_value = booking_db
    result = BookingService(mock_get_db).get_booking_by_user(1023952)
    assert result is not None
    assert result.delivery_address == booking["delivery_address"]


@pytest.mark.unit
@patch("core.services.booking_service.BookingService.get_user_info")
def test_service_get_user_info(mock_get_user_info, mock_get_db):
    user = user_info()
    user_db = User(**user)
    mock_get_user_info.return_value = user_db
    result = BookingService(mock_get_db).get_user_info("test@gmail.com")
    assert result is not None
    assert result.id == user["id"]


@pytest.mark.unit
@patch("core.services.booking_service.BookingService.get_product_info")
def test_service_get_product_info(mock_get_product_info, mock_get_db):
    product = product_info()
    product_db = Product(**product)
    mock_get_product_info.return_value = product_db
    result = BookingService(mock_get_db).get_product_info("Test Book")
    assert result is not None
    assert result.id == product_db.id


@pytest.mark.unit
@patch("core.services.booking_service.BookingService.get_status_id")
def test_service_get_status_info(mock_get_status_info, mock_get_db):
    status = status_info()
    status_db = Status(**status)
    mock_get_status_info.return_value = status_db
    result = BookingService(mock_get_db).get_status_id("SUBMITTED")
    assert result is not None
    assert result.id == status_db.id


@pytest.mark.unit
@patch("core.services.booking_service.BookingService.update_booking")
def test_service_update_booking(mock_update_booking, mock_get_db):
    booking = booking_info()
    booking_db = Booking(**booking)
    booking_up = booking_update()
    mock_update_booking.return_value = booking_up
    result = BookingService(mock_get_db).update_booking(booking_db, booking_up)
    assert result is not None
    assert result.delivery_time == booking_up.delivery_time


@pytest.mark.unit
@patch("core.services.booking_service.BookingService.delete_booking")
def test_service_delete_booking(mock_delete_booking, mock_get_db):
    booking = booking_info()
    booking_db = Booking(**booking)
    mock_delete_booking.return_value = ""
    result = BookingService(mock_get_db).delete_booking(booking_db)
    assert result == ""
