from random import randint
import requests

import pytest
from core.schema.user_dto import UserDTO


def test_user():
    # Add new user
    user_id: int = 102395 + randint(0,999)
    email: str = str(str(randint(0,999)) + 'test@gmail.com')
    user_dto: UserDTO = UserDTO(
        id=user_id,
        name='Andrea',
        email=email,
        phone='2458794',
        address='carrera xxx',
        login=email,
        password='12345')

    # Call endpoint

