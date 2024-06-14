from sqlalchemy import create_engine

from config.Enums import StatusEnum, RolesEnum
from config.database import DBConnection
from core.config import Config
from core.models.role_model import Role
from core.models.status_model import Status
from config.database import Base

cfg: Config = Config()
env: str = cfg.ENV


def add_status(session):
    validate: bool = bool(session.query(Status).filter(Status.name == StatusEnum.SUBMITTED.value).first())
    if not validate:
        for i in StatusEnum:
            session.add(Status(name=i.value))
            session.commit()


def add_roles(session):
    validate: bool = bool(session.query(Role).filter(Role.name == RolesEnum.CUSTOMER.value).first())
    if not validate:
        for i in RolesEnum:
            session.add(Role(name=i.value))
            session.commit()


def database():
    if cfg.MODE_TEST == 'DEVELOP':
        database_url: str = cfg.get_environment_config(env)
        engine = create_engine(database_url, echo=True)
        Base.metadata.create_all(bind=engine)
        db = DBConnection().connect_db()
        add_status(db)
        add_roles(db)



