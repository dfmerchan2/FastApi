from typing import Optional

from pydantic import BaseModel


class ProductStoreUpdateDTO(BaseModel):
    availability_qty: Optional[int] = None
    booked_qty: Optional[int] = None
    sold_qty: Optional[int] = None


class ProductStoreDTO(BaseModel):
    availability_qty: int
    booked_qty: int
    sold_qty: int
