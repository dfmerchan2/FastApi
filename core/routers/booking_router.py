from typing import List, Optional

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse
from fastapi import Body, Depends

from config.Enums import RolesEnum
from core.authenticator.jwt_bearer import JWTBearer
from core.authenticator.role_checker import RoleChecker
from core.schema.booking_dto import BookingDTO, BookingUpdateDTO, StatusDTO
from core.models.booking_model import Booking
from core.services.booking_service import BookingService

from config.database import DBConnection

booking_router = APIRouter()
db = DBConnection().connect_db()
jwt = JWTBearer()


@booking_router.get('/bookings', tags=['Booking'], response_model=List[BookingDTO], status_code=200)
def get_bookings(current_user=Depends(RoleChecker([RolesEnum.MANAGER.value]))):
    result = BookingService(db).get_booking()
    return JSONResponse(content=jsonable_encoder(result))


@booking_router.get('/booking/', tags=['Booking'], response_model=BookingDTO, status_code=200)
def get_booking_by_id_or_user(id_booking: Optional[int] = None, user_id: Optional[int] = None, current_user=Depends(RoleChecker([RolesEnum.MANAGER.value, RolesEnum.CUSTOMER.value]))):
    if id_booking:
        result = BookingService(db).get_booking_by_id(id_booking)
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Booking not found')
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
    else:
        result = BookingService(db).get_booking_by_user(user_id)
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Booking not found for the user')
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@booking_router.post('/booking/create', tags=['Booking'], status_code=201)
def create_new_booking(product_name: str, status_req: str = "SUBMITTED", current_user=Depends(RoleChecker([RolesEnum.MANAGER.value, RolesEnum.CUSTOMER.value])), booking: BookingDTO = Body()):
    booking_dict = booking.dict()
    user_data = BookingService(db).get_user_info(current_user['login'])
    booking_dict['user_id'] = user_data.id
    product_data = BookingService(db).get_product_info(product_name)
    booking_dict['product_id'] = product_data.id
    status_query = BookingService(db).get_status_name(status_req)
    booking_dict['status_id'] = status_query.id
    new_booking = Booking(**booking_dict)
    BookingService(db).create_booking(new_booking)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Booking register successfully")


@booking_router.put('/booking/update', tags=['Booking'], status_code=200)
def update_booking(id_booking: int, status_req: str, booking_dto: BookingUpdateDTO, current_user=Depends(RoleChecker([RolesEnum.MANAGER.value, RolesEnum.CUSTOMER.value]))):
    booking_dict = booking_dto.dict()
    status_query = BookingService(db).get_status_name(status_req)
    booking_dict["status_id"] = status_query.id
    result = BookingService(db).get_booking_by_id(id_booking)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Booking not found')
    else:
        update = BookingService(db).update_booking(result, booking_dict)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(update))


@booking_router.delete('/booking/delete', tags=['Booking'], status_code=200)
def delete_booking(id_booking: int, current_user=Depends(RoleChecker([RolesEnum.MANAGER.value, RolesEnum.CUSTOMER.value]))):
    result = BookingService(db).get_booking_by_id(id_booking)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Booking not found')
    else:
        BookingService(db).delete_booking(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content='Booking was deleted')

