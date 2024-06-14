from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from config.Enums import RolesEnum
from config.database import DBConnection
from core.authenticator.jwt_bearer import JWTBearer
from core.authenticator.role_checker import RoleChecker
from core.models.product_store_model import ProductStore
from core.services.product_service import ProductService
from core.services.product_store_service import ProductStoreService
from core.schema.product_store_dto import ProductStoreDTO, ProductStoreUpdateDTO

store_router = APIRouter()
db = DBConnection().connect_db()
jwt = JWTBearer()


@store_router.get('/product/store', tags=['Products Store'])
def get_products_store(current_user=Depends(RoleChecker([RolesEnum.MANAGER.value]))):
    result = ProductStoreService(db).get_products_store()
    return JSONResponse(content=jsonable_encoder(result))


@store_router.get('/product/store/', tags=['Products Store'], response_model=ProductStoreDTO, status_code=200)
def get_product_store_by_id(product_store_id: int, current_user=Depends(RoleChecker([RolesEnum.MANAGER.value]))):
    result = ProductStoreService(db).get_product_store_by_id(product_store_id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Product store not found')
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@store_router.post('/store/create', tags=['Products Store'], status_code=201)
def create_new_product_store(product_name: str, product_dto: ProductStoreDTO = Body(), current_user=Depends(RoleChecker([RolesEnum.MANAGER.value]))):
    product_dict = product_dto.dict()
    product = ProductService(db).get_product_by_name(product_name)
    product_dict["product_id"] = product.id
    new_store = ProductStore(**product_dict)
    ProductStoreService(db).create_product_store(new_store)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Product Store register successfully")


@store_router.put('/store/update', tags=['Products Store'], status_code=200)
def update_product_store(product_store_id: int, product_dto: ProductStoreUpdateDTO, current_user=Depends(RoleChecker([RolesEnum.MANAGER.value]))):
    result = ProductStoreService(db).get_product_store_by_id(product_store_id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Store not found')
    else:
        update = ProductStoreService(db).update_product_store(result, product_dto)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(update))


@store_router.delete('/store/delete', tags=['Products Store'], status_code=200)
def delete_product_store(product_store_id: int, current_user=Depends(RoleChecker([RolesEnum.MANAGER.value]))):
    result = ProductStoreService(db).get_product_store_by_id(product_store_id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Store not found')
    else:
        ProductStoreService(db).delete_product_store(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content='Store was deleted')
