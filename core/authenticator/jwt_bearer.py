from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import joinedload

from core.authenticator.jwt_manager import validate_token
from config.database import DBConnection
from core.models.user_model import User
from core.models.role_model import Role


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        db = DBConnection().connect_db()
        try:
            user = db.query(User).filter(User.email == data['login']).first()
            role_user_db = db.query(Role).outerjoin(User).filter(user.role_id == Role.id).first()
        except Exception:
            raise HTTPException(status_code=404, detail="Verify your data or you are not registered")
        if role_user_db.name != data['role'].upper():
            raise HTTPException(status_code=403, detail="Invalid Role")
        elif data['password'] != user.password:
            raise HTTPException(status_code=403, detail="Invalid Credentials")
        else:
            return data

