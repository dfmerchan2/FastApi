from typing import List

from fastapi import Depends, HTTPException
from starlette import status

from core.authenticator.jwt_bearer import JWTBearer

jwt = JWTBearer()


class RoleChecker:

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: dict = Depends(jwt)):
        if current_user['role'].upper() not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
        return current_user
