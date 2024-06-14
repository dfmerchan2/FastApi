from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from config.database import DBConnection
from core.authenticator.jwt_manager import create_token
from core.schema.user_dto import LoginDTO
from starlette.responses import JSONResponse


auth_router = APIRouter()


@auth_router.post('/login', tags=['Auth'])
def auth(role: str, user: LoginDTO):
    login_dict = user.dict()
    login_dict["role"] = role
    token = create_token(login_dict)
    return JSONResponse(status_code=200, content=jsonable_encoder(token))



