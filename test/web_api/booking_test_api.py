from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from core.models.booking_model import Booking
from core.models.products_model import Product
from core.models.status_model import Status
from core.models.user_model import User
from core.authenticator.role_checker import jwt
from main import app
from test.conftest.mocks_apis import get_jwt_manager, get_jwt_customer, get_jwt_admin, booking_req_info, \
    booking_update_req_info
from test.conftest.mocks_services import booking_info, user_info, product_info, status_info

client = TestClient(app)


@pytest.mark.api
@patch("core.services.booking_service.BookingService.get_booking")
def test_get_bookings_api(mock_get_booking):
    app.dependency_overrides[jwt] = get_jwt_manager
    booking_mock = booking_info()
    mock_get_booking.return_value = [Booking(**booking_mock)]
    resp = client.get(url=f'/bookings', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json()[0] == booking_mock


@pytest.mark.api
def test_get_bookings_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_customer
    resp = client.get(url=f'/bookings', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.booking_service.BookingService.get_booking_by_id")
def test_get_booking_by_id_api(mock_get_booking):
    app.dependency_overrides[jwt] = get_jwt_manager
    booking_mock = booking_info()
    mock_get_booking.return_value = Booking(**booking_mock)
    resp = client.get(url=f'/booking/?id_booking=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json() == booking_mock


@pytest.mark.api
@patch("core.services.booking_service.BookingService.get_booking_by_user")
def test_get_booking_by_user_api(mock_get_booking):
    app.dependency_overrides[jwt] = get_jwt_manager
    booking_mock = booking_info()
    mock_get_booking.return_value = [Booking(**booking_mock)]
    resp = client.get(url=f'/booking/?user_id=102395', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json()[0] == booking_mock


@pytest.mark.api
def test_get_bookings_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    resp = client.get(url=f'/booking/?user_id=102395', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.booking_service.BookingService.get_booking_by_id")
def test_get_booking_by_id_api_not_found(mock_booking):
    app.dependency_overrides[jwt] = get_jwt_customer
    mock_booking.return_value = ""
    resp = client.get(url=f'/booking/?id_booking=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 404
    assert resp.json() == 'Booking not found'


@pytest.mark.api
@patch("core.services.booking_service.BookingService.get_booking_by_user")
def test_get_booking_by_user_id_api_not_found(mock_booking):
    app.dependency_overrides[jwt] = get_jwt_customer
    mock_booking.return_value = ""
    resp = client.get(url=f'/booking/?user_id=102395', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 404
    assert resp.json() == 'Booking not found for the user'


@pytest.mark.api
@patch("core.services.status_service.StatusService.get_status_by_name")
@patch("core.services.booking_service.BookingService.get_user_info")
@patch("core.services.booking_service.BookingService.get_product_info")
@patch("core.services.booking_service.BookingService.get_status_name")
@patch("core.services.booking_service.BookingService.create_booking")
def test_create_booking_api(mock_status_name,mock_user, mock_product, mock_status, mock_booking):
    app.dependency_overrides[jwt] = get_jwt_manager
    booking_req = booking_req_info()
    booking_mock = booking_info()
    user_mock = user_info()
    prod_mock = product_info()
    status_mock = status_info()
    mock_status_name.return_value = ""
    mock_user.return_value = User(**user_mock)
    mock_product.return_value = Product(**prod_mock)
    mock_status.return_value = Status(**status_mock)
    mock_booking.return_value = Booking(**booking_mock)
    resp = client.post(url=f'/booking/create?product_name=Test', headers={"Authorization": f"Bearer TestAuto"}, content=booking_req)
    assert resp.status_code == 201
    assert resp.json() == "Booking register successfully"


@pytest.mark.api
@patch("core.services.status_service.StatusService.get_status_by_name")
@patch("core.services.status_service.StatusService.add_status")
def test_create_booking_api_unauthorized(mock_status_name, mock_add_status):
    app.dependency_overrides[jwt] = get_jwt_admin
    mock_status_name.return_value = ""
    mock_add_status.return_value = ""
    booking_req = booking_req_info()
    resp = client.post(url=f'/booking/create?product_name=Test', headers={"Authorization": f"Bearer TestAuto"}, content=booking_req)
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.booking_service.BookingService.get_booking_by_id")
@patch("core.services.booking_service.BookingService.get_status_name")
@patch("core.services.booking_service.BookingService.update_booking")
def test_update_booking_api(mock_get_booking, mock_status, mock_booking):
    app.dependency_overrides[jwt] = get_jwt_manager
    booking_req = booking_update_req_info()
    booking_mock = booking_info()
    status_mock = status_info()
    mock_get_booking.return_value = Booking(**booking_mock)
    mock_status.return_value = Status(**status_mock)
    mock_booking.return_value = Booking(**booking_mock)
    resp = client.put(url=f'/booking/update?id_booking=1&status_req=SUBMITTED', headers={"Authorization": f"Bearer TestAuto"}, content=booking_req)
    assert resp.status_code == 200
    assert resp.json() == booking_mock


@pytest.mark.api
def test_update_booking_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    booking_req = booking_update_req_info()
    resp = client.put(url=f'/booking/update?id_booking=1&status_req=2', headers={"Authorization": f"Bearer TestAuto"}, content=booking_req)
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.booking_service.BookingService.get_status_name")
@patch("core.services.booking_service.BookingService.get_booking_by_id")
def test_update_booking_api_not_found(mock_booking, mock_status):
    app.dependency_overrides[jwt] = get_jwt_customer
    status_mock = status_info()
    mock_status.return_value = Status(**status_mock)
    mock_booking.return_value = ""
    booking_req = booking_update_req_info()
    resp = client.put(url=f'/booking/update?id_booking=1&status_req=2', headers={"Authorization": f"Bearer TestAuto"},
                      content=booking_req)
    assert resp.status_code == 404
    assert resp.json() == 'Booking not found'


@pytest.mark.api
@patch("core.services.booking_service.BookingService.get_booking_by_id")
@patch("core.services.booking_service.BookingService.delete_booking")
def test_delete_booking_api(mock_booking, mock_get_booking):
    app.dependency_overrides[jwt] = get_jwt_manager
    booking_mock = booking_info()
    mock_get_booking.return_value = Booking(**booking_mock)
    mock_booking.return_value = ""
    resp = client.delete(url=f'/booking/delete?id_booking=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 200
    assert resp.json() == "Booking was deleted"


@pytest.mark.api
def test_delete_booking_api_unauthorized():
    app.dependency_overrides[jwt] = get_jwt_admin
    resp = client.delete(url=f'/booking/delete?id_booking=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 401
    assert str(resp.json()) == """{'detail': 'Unauthorized'}"""


@pytest.mark.api
@patch("core.services.booking_service.BookingService.get_booking_by_id")
def test_delete_booking_api_not_found(mock_booking):
    app.dependency_overrides[jwt] = get_jwt_customer
    mock_booking.return_value = ""
    resp = client.delete(url=f'/booking/delete?id_booking=1', headers={"Authorization": f"Bearer TestAuto"})
    assert resp.status_code == 404
    assert resp.json() == 'Booking not found'
