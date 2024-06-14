from typing import Optional

from pydantic import BaseModel


class ProductUpdateDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    image_path: Optional[str] = None


class ProductDTO(BaseModel):
    name: str
    description: str
    author: str
    price: float
    image_path: str
