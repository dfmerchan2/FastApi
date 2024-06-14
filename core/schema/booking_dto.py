from typing import Optional

from pydantic import BaseModel


class StatusDTO(BaseModel):
    name: str


class BookingUpdateDTO(BaseModel):
    delivery_address: Optional[str] = None
    delivery_date: Optional[str] = None
    delivery_time: Optional[str] = None
    quantity: Optional[int] = None


class BookingDTO(BaseModel):
    delivery_address: str
    delivery_date: str
    delivery_time: str
    quantity: int
