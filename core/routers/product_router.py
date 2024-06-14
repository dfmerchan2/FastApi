from typing import List

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from config.Enums import RolesEnum
from config.database import DBConnection
from core.authenticator.jwt_bearer import JWTBearer
from core.authenticator.role_checker import RoleChecker
from core.models.products_model import Product
from core.services.product_service import ProductService
from core.schema.product_dto import ProductUpdateDTO, ProductDTO

product_router = APIRouter()
db = DBConnection().connect_db()


@product_router.get('/products', tags=['Products'], response_model=List[ProductDTO])
def get_products(current_user=Depends(RoleChecker([RolesEnum.MANAGER.value, RolesEnum.CUSTOMER.value]))):
    result = ProductService(db).get_product()
    return JSONResponse(content=jsonable_encoder(result))


@product_router.get('/product', tags=['Products'], response_model=ProductDTO, status_code=200)
def get_product_by_name(product_name: str, current_user=Depends(RoleChecker([RolesEnum.MANAGER.value, RolesEnum.CUSTOMER.value]))):
    result = ProductService(db).get_product_by_name(product_name)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Product not found')
    else:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@product_router.post('/product/create', tags=['Products'], status_code=201)
def create_new_product(product_dto: ProductDTO = Body(), current_user=Depends(RoleChecker([RolesEnum.MANAGER.value]))):
    new_product = Product(**product_dto.dict())
    ProductService(db).create_product(new_product)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Product register successfully")


@product_router.put('/product/update', tags=['Products'], status_code=200)
def update_product(product_id: int, product_dto: ProductUpdateDTO, current_user=Depends(RoleChecker([RolesEnum.MANAGER.value]))):
    result = ProductService(db).get_product_by_id(product_id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Product not found')
    else:
        update = ProductService(db).update_product(result, product_dto)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(update))


@product_router.delete('/product/delete', tags=['Products'], status_code=200)
def delete_product(product_id: int, current_user=Depends(RoleChecker([RolesEnum.MANAGER.value]))):
    result = ProductService(db).get_product_by_id(product_id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Product not found')
    else:
        ProductService(db).delete_product(result)
        return JSONResponse(status_code=status.HTTP_200_OK, content='Product was deleted')
