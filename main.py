
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from config.base_db import database
from core.routers.auth_router import auth_router
from core.routers.user_router import usr_router
from core.routers.booking_router import booking_router
from core.routers.product_router import product_router
from core.routers.product_store_router import store_router
from reactpy.backend.fastapi import configure

from core.web_ui.home_page import HomePage

database()
app = FastAPI()
app.include_router(auth_router)
app.include_router(usr_router)
app.include_router(booking_router)
app.include_router(product_router)
app.include_router(store_router)
configure(app, HomePage)




