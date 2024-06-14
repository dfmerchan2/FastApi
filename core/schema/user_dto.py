from typing import Optional

from pydantic import BaseModel


class LoginDTO(BaseModel):
    login: str
    password: str


class RoleDTO(BaseModel):
    name: str


class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserDTO(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str
    login: str
    password: str


class UserOutputDTO(BaseModel):
    id: int
    name: str
    email: str
    role_id: int
    phone: str
    address: str
    login: str
    password: str
