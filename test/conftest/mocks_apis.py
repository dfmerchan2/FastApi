import json

from core.schema.booking_dto import BookingDTO, BookingUpdateDTO
from core.schema.product_dto import ProductDTO, ProductUpdateDTO
from core.schema.product_store_dto import ProductStoreDTO, ProductStoreUpdateDTO
from core.schema.user_dto import UserDTO, RoleDTO, UserUpdateDTO


def get_jwt_admin():
    info = dict([("login", "test@gmail.com"), ("password", "12345"), ("role", "Admin")])
    return info


def get_jwt_customer():
    info = dict([("login", "test@gmail.com"), ("password", "12345"), ("role", "Customer")])
    return info


def get_jwt_manager():
    info = dict([("login", "test@gmail.com"), ("password", "12345"), ("role", "Manager")])
    return info


def user_req_api():
    user_dto = UserDTO(
        id=1023952,
        name="testuser",
        email="test@gmail.com",
        phone="12345",
        address="Carrera12",
        login="test@gmail.com",
        password="12345")
    user_dict = user_dto.model_dump()
    user_json = json.dumps(user_dict)
    return user_json


def role_info():
    role_dto = RoleDTO(
        name="Admin"
    )
    role_dict = role_dto.model_dump()
    return role_dict


def user_update_req_api():
    user_dto = UserUpdateDTO(
        name="testuser",
        phone="2451525",
        address="Carrera12")
    user_dict = user_dto.model_dump()
    user_json = json.dumps(user_dict)
    return user_json


def product_req_api():
    product_dto = ProductDTO(
        name="Test book",
        description="This book is to learn about testing",
        author="test author",
        price=2.58,
        image_path="/url/test"
    )
    prod_dict = product_dto.model_dump()
    prod_json = json.dumps(prod_dict)
    return prod_json


def product_update_req_api():
    product_dto = ProductUpdateDTO(
        name="Test book update",
        description="Description updaye",
        author="test author update",
        price=2.87,
        image_path="/url/test/update"
    )
    prod_dict = product_dto.model_dump()
    prod_json = json.dumps(prod_dict)
    return prod_json


def store_req_api():
    store_dto = ProductStoreDTO(
        availability_qty=10,
        booked_qty=0,
        sold_qty=0
    )
    store_dict = store_dto.model_dump()
    store_json = json.dumps(store_dict)
    return store_json


def store_update_req_api():
    store_dto = ProductStoreUpdateDTO(
        availability_qty=10,
        booked_qty=0,
        sold_qty=0
    )
    store_dict = store_dto.model_dump()
    store_json = json.dumps(store_dict)
    return store_json


def booking_req_info():
    booking_dto = BookingDTO(
        delivery_address="Carrera test",
        delivery_date="12/09/2024",
        delivery_time="12:00",
        quantity=2
    )
    booking_dict = booking_dto.model_dump()
    booking_json = json.dumps(booking_dict)
    return booking_json


def booking_update_req_info():
    booking_dto = BookingUpdateDTO(
        delivery_address="Carrera test",
        delivery_date="13/09/2024",
        delivery_time="12:00",
        quantity=2
    )
    booking_dict = booking_dto.model_dump()
    booking_json = json.dumps(booking_dict)
    return booking_json