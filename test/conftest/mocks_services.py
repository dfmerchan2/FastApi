from core.models.user_model import User
from core.schema.booking_dto import BookingDTO, StatusDTO, BookingUpdateDTO
from core.schema.product_dto import ProductDTO, ProductUpdateDTO
from core.schema.product_store_dto import ProductStoreDTO, ProductStoreUpdateDTO
from core.schema.user_dto import UserDTO, UserOutputDTO, UserUpdateDTO


def user_info():
    user_dto = UserOutputDTO(
        id=1023952,
        name="testuser",
        email="test@gmail.com",
        phone="12345",
        role_id=1,
        address="Carrera12",
        login="test@gmail.com",
        password="12345")
    user_dict = user_dto.model_dump()
    return user_dict


def user_update():
    user_dto = UserUpdateDTO(
        name="testUpdate"
    )
    return user_dto


def product_info():
    product_dto = ProductDTO(
        name="Test book",
        description="This book is to learn about testing",
        author="test author",
        price=2.58,
        image_path="/url/test"
    )
    product_dict = product_dto.model_dump()
    product_dict["id"] = 1
    return product_dict


def product_update():
    product_dto = ProductUpdateDTO(
        name="Test book update",
        description="Description updaye",
        author="test author update",
        price=2.87,
        image_path="/url/test/update"
    )
    return product_dto


def product_store_info():
    store_dto = ProductStoreDTO(
        availability_qty=10,
        booked_qty=0,
        sold_qty=0
    )
    store_dict=store_dto.model_dump()
    return store_dict


def product_store_update():
    store_dto = ProductStoreUpdateDTO(
        availability_qty=15
    )
    return store_dto


def booking_info():
    booking_dto = BookingDTO(
        delivery_address="Carrera test",
        delivery_date="12/09/2024",
        delivery_time="12:00",
        quantity=2
    )
    booking_dict = booking_dto.model_dump()
    return booking_dict


def status_info():
    status_dto = StatusDTO(
        name="SUBMITTED"
    )
    status_dict=status_dto.model_dump()
    status_dict["id"] = 2
    return status_dict


def booking_update():
    booking_dto = BookingUpdateDTO(
        delivery_time="13:00"
    )
    return booking_dto