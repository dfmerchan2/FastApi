from jwt import encode, decode

from core.config import Config

cfg: Config = Config()


def create_token(data: dict) -> str:
    token: str = encode(payload=data, key=cfg.SECRET_KEY, algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    data: dict = decode(token, key=cfg.SECRET_KEY, algorithms=['HS256'])
    return data
