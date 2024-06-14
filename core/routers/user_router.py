from fastapi import APIRouter
from typing import List

from config.Enums import RolesEnum
from core.authenticator.role_checker import RoleChecker
from core.schema.user_dto import UserDTO, UserUpdateDTO, RoleDTO, UserOutputDTO
from fastapi import Body, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status

from config.database import DBConnection
from core.models.user_model import User
from core.services.user_service import UserService

usr_router = APIRouter()
db = DBConnection().connect_db()


@usr_router.get('/users', tags=['User'], response_model=List[UserOutputDTO], status_code=200)
def get_users(current_user=Depends(RoleChecker([RolesEnum.ADMIN.value]))):
    result = UserService(db).get_users()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@usr_router.get('/user/id/', tags=['User'], response_model=UserOutputDTO, status_code=200)
def get_user_by_id(id_user: int, current_user=Depends(RoleChecker([RolesEnum.ADMIN.value, RolesEnum.CUSTOMER.value]))):
    result = UserService(db).get_user_by_id(id_user)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Id not found')
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@usr_router.post('/user/create', tags=['User'], status_code=201)
def create_new_user(role: str, user: UserDTO = Body()):
    user_with_role = user.dict()
    if role.upper() == RolesEnum.ADMIN:
        user_with_role['role_id'] = 1
    elif role.upper() == RolesEnum.MANAGER:
        user_with_role['role_id'] = 2
    else:
        user_with_role['role_id'] = 3
    new_user = User(**user_with_role)
    UserService(db).create_user(new_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="User register successfully")


@usr_router.put('/user/update', tags=['User'], status_code=200)
def update_user(id_user: int, user: UserUpdateDTO, current_user=Depends(RoleChecker([RolesEnum.ADMIN.value, RolesEnum.CUSTOMER.value]))):
    result = UserService(db).get_user_by_id(id_user)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Id not found')
    else:
        update = UserService(db).update_user(result, user)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(update))


@usr_router.delete('/user/delete', tags=['User'], status_code=200)
def delete_user(id_user: int, current_user=Depends(RoleChecker([RolesEnum.ADMIN.value, RolesEnum.CUSTOMER.value]))):
    result = UserService(db).get_user_by_id(id_user)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Id not found')
    else:
        UserService(db).delete_user(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content='User was deleted')

